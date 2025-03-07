from sqlalchemy.orm import Session
import models
import schemas
from datetime import datetime

# Пользователи
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = "fake_hashed_password"  # Замени на реальный хэш
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Посты
def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

# Комментарии
def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(**comment.dict(), user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Лайки
def create_like(db: Session, like: schemas.LikeCreate, user_id: int):
    db_like = models.Like(**like.dict(), user_id=user_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

# Сообщества
def create_community(db: Session, community: schemas.CommunityCreate, owner_id: int):
    db_community = models.Community(**community.dict(), owner_id=owner_id)
    db.add(db_community)
    db.commit()
    db.refresh(db_community)
    return db_community

def join_community(db: Session, community_member: schemas.CommunityMemberCreate, user_id: int):
    db_member = models.CommunityMember(**community_member.dict(), user_id=user_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_communities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Community).offset(skip).limit(limit).all()

# Уведомления
def create_notification(db: Session, notification: schemas.NotificationCreate, user_id: int):
    db_notification = models.Notification(**notification.dict(), user_id=user_id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).offset(skip).limit(limit).all()

# Черный список токенов
def add_token_to_blacklist(db: Session, token: str, expires_at: datetime):
    db_token = models.BlacklistedToken(token=token, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def is_token_blacklisted(db: Session, token: str):
    return db.query(models.BlacklistedToken).filter(models.BlacklistedToken.token == token).first()