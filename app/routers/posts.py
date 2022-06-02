from fastapi import (
    Response, status, HTTPException, Depends, APIRouter
)
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from app import oauth2
from .. import schema, models
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


# --------------- request Get Methods

@router.get(
    "/", response_model=List[schema.PostVotes]
)
# @router.get("/")
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    search: Optional[str] = '',
    limit: int = 10,
    skip: int = 0,
):

    posts = (
        db.query(models.Post, func.count(models.Votes.post_id).label('likes'))
        .join(
            models.Votes,
            models.Votes.post_id == models.Post.id,
            isouter=True
        )
        .group_by(models.Post.id)
        .filter(models.Post.content.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Posts collection is empty"
        )

    return posts


@router.get(
    "/{id}", response_model=schema.PostVotes
)
def get_post(
        id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):

    post = (
        db.query(models.Post, func.count(models.Votes.post_id).label('likes'))
        .join(
            models.Votes,
            models.Votes.post_id == models.Post.id,
            isouter=True
        )
        .group_by(models.Post.id)
        .filter(models.Post.id == id).first()
    )

    if post is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found"
        )

    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schema.Post
)
def create_post(
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post_id: {id} is missing"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authorized to perform request action'
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --------------- request Update

@router.put(
    "/{id}", response_model=schema.Post
)
def update_post(
    id: int,
    upd_post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post_id: {id} is missing"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authorized to perform request action'
        )

    post_query.update(upd_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
