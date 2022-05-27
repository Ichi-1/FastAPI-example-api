from pydantic import BaseModel, EmailStr, conint
from pydantic.class_validators import validator
from datetime import datetime
from fastapi import HTTPException, status
from validate_email import validate_email
import typing



"""  Users """

class UserCreate(BaseModel):
    email = 'Missing Field'
    password = 'Missing Field'

    # class Config:
    #     orm_mode = True


    @validator('email')
    def is_email_empty(cls, credential):
        if not credential:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email field cannot be empty'
            )
        elif not validate_email(credential):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email is not valid'
            )
        return credential
        
    @validator('password')
    def is_password_short(cls, password):
        if len(password) < 4:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password must be at least 4 characters long'
        )
        return password

    



class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str



""" Posts """

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


""" Tokens """

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: typing.Optional[str] = None



""" Votes """

class Vote(BaseModel):
    post_id: int
    state: conint(le=1)
