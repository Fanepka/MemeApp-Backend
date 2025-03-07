from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Модели для пользователя
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Заменяем orm_mode = True

# Модели для поста
class PostBase(BaseModel):
    text: str
    image_url: Optional[str] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Модели для комментария
class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Модели для лайка
class LikeBase(BaseModel):
    post_id: int

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Модели для сообщества
class CommunityBase(BaseModel):
    name: str
    description: str

class CommunityCreate(CommunityBase):
    pass

class Community(CommunityBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Модели для участника сообщества
class CommunityMemberBase(BaseModel):
    community_id: int

class CommunityMemberCreate(CommunityMemberBase):
    pass

class CommunityMember(CommunityMemberBase):
    id: int
    user_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Модели для уведомления
class NotificationBase(BaseModel):
    message: str

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    user_id: int
    created_at: datetime
    is_read: bool

    model_config = ConfigDict(from_attributes=True)

# Модели для токенов
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None