from pydantic import BaseModel, EmailStr, conint, ValidationError
from pydantic.class_validators import validator
from datetime import datetime
import typing



# -----------> Users

class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str



# -----------> Posts

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostVotes(BaseModel):
    Post: Post
    likes: int

    class Config:
        orm_mode = True


# -----------> Posts Token Schemas

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: typing.Optional[str] = None



# -----------> Vote 

class Vote(BaseModel):
    post_id: int
    state: conint(le=1)
