from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt, JWTError
from database import SessionLocal, engine
import models
import schemas
import crud
from auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
    token_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
)

# Создание таблиц в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Регистрация пользователя
@app.post("/auth/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Авторизация и получение токенов

@app.post("/auth/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



# Обновление токена
@app.post("/auth/refresh-token", response_model=schemas.Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    new_refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

# Выход из системы
@app.post("/auth/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires_at = datetime.fromtimestamp(payload["exp"])
        crud.add_token_to_blacklist(db, token, expires_at)
        return {"message": "Successfully logged out"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

# Получение информации о текущем пользователе
@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

# Создание поста
@app.post("/posts/", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):  
    user = token_user(db, current_user['email'])
    return crud.create_post(db=db, post=post, user_id=user.id)

# Получение списка постов
@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

# Лайк поста
@app.post("/posts/{post_id}/like", response_model=schemas.Like)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.create_like(db=db, like=schemas.LikeCreate(post_id=post_id), user_id=current_user.id)

# Комментирование поста
@app.post("/posts/{post_id}/comment", response_model=schemas.Comment)
def comment_post(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id)

# Создание сообщества
@app.post("/communities/", response_model=schemas.Community)
def create_community(
    community: schemas.CommunityCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_community(db=db, community=community, owner_id=current_user.id)

# Присоединение к сообществу
@app.post("/communities/{community_id}/join", response_model=schemas.CommunityMember)
def join_community(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.join_community(db=db, community_member=schemas.CommunityMemberCreate(community_id=community_id), user_id=current_user.id)

# Получение списка сообществ
@app.get("/communities/", response_model=list[schemas.Community])
def read_communities(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    communities = crud.get_communities(db, skip=skip, limit=limit)
    return communities

# Создание уведомления
@app.post("/notifications/", response_model=schemas.Notification)
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_notification(db=db, notification=notification, user_id=current_user.id)

# Получение списка уведомлений
@app.get("/notifications/", response_model=list[schemas.Notification])
def read_notifications(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    notifications = crud.get_notifications(db, user_id=current_user.id, skip=skip, limit=limit)
    return notifications

# Поиск постов
@app.get("/search/posts", response_model=list[schemas.Post])
def search_posts(
    query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    posts = db.query(models.Post).filter(models.Post.text.contains(query)).offset(skip).limit(limit).all()
    return posts

# Поиск пользователей
@app.get("/search/users", response_model=list[schemas.User])
def search_users(
    query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    users = db.query(models.User).filter(models.User.username.contains(query)).offset(skip).limit(limit).all()
    return users

# Поиск сообществ
@app.get("/search/communities", response_model=list[schemas.Community])
def search_communities(
    query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    communities = db.query(models.Community).filter(models.Community.name.contains(query)).offset(skip).limit(limit).all()
    return communities