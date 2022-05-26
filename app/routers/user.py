from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from validate_email import validate_email

from .. import schema, models, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users'],
)


@router.post("/sign-in", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    # email validation 
    if not user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email cannot be empty'
        )

    if not validate_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid email format'
        )

    # password validation
    if len(user.password) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password must be at least 4 characters long '
        )

    # если юзер уже есть - 400 
    is_user_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if is_user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{user.email} already registered'
        )
    
    
    hash_pwd = utils.hash(user.password)
    user.password = hash_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get("/{id}", response_model=schema.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} does not exist"
        )
    return user