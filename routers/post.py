from fastapi import status, HTTPException, Response, Depends, APIRouter
from schemas import PostCreate, Post
from typing import List
from database import get_db
from sqlalchemy.orm import Session
import models


router = APIRouter()

@router.get("/post", response_model=List[Post])
async def posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.Post).all()
    return all_posts


@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exit",
        )

    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
