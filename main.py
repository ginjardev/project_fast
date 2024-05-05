from fastapi import FastAPI, Body, status, HTTPException, Response, Depends
from schemas import PostCreate, Post
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from models import Base
from database import engine, get_db
from sqlalchemy.orm import Session
import models


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/post")
async def posts(db: Session = Depends(get_db)):
	all_posts = db.query(models.Post).all()
	return all_posts


@app.post('/post', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=Post)
def get_post(id:int, db: Session=Depends(get_db)):
	post = db.query(models.Post).filter(models.Post.id==id).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
					  		detail=f"Post with id: {id} not found")
	return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id==id).first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
					  detail=f"Post with id {id} does not exit")

    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
