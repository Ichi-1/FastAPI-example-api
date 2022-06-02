from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm as OAuth2
from sqlalchemy.orm import Session
from .. import schema, models, database, utils, oauth2


router = APIRouter(
    prefix='/users',
    tags=['Auth']
)


@router.post(
    '/login', response_model=schema.Token
)
def login(
    user_credentials: OAuth2 = Depends(),
    db: Session = Depends(database.get_db)
):

    user = db.query(models.User) \
        .filter(models.User.email == user_credentials.username).first()

    # user validation
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid credentials'
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid credentials'
        )
    access_token = oauth2.create_access_token(payload={"user_id": user.id})

    return {"access_token": access_token, "token_type": "Bearer"}
