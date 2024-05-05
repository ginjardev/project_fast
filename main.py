from fastapi import FastAPI, Body, status, HTTPException, Response, Depends
from pydantic import BaseModel
from typing import Optional
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


while True:
	try:
		conn = psycopg2.connect(database='fastapidb', user='postgres', password='postgres', cursor_factory=RealDictCursor)
		cursor = conn.cursor()
		print("o wa okay!")
		break
	except Exception as e:
		print("DB connection failed")
		print(e.args)
		time.sleep(3)

class Post(BaseModel):
	id: Optional[int] = None
	title: str
	content: str
	published: bool = True


@app.get("/post")
async def posts(db: Session = Depends(get_db)):
    # cursor.execute(
    # 	"""SELECT * FROM posts;"""
    # )
    # posts = cursor.fetchall()
	all_posts = db.query(models.Post).all()
	return {"posts": all_posts}


@app.post('/post', status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
	cursor.execute(
		"""INSERT INTO posts (title, content, published)
		VALUES (%s, %s, %s) RETURNING *;
		""", 
		(post.title, post.content, post.published)
	)
	new_post = cursor.fetchone()
	conn.commit()
	return {"post": new_post}

@app.get("/posts/{id}")
def get_post(id:int):
	cursor.execute(
		"""SELECT * FROM posts WHERE id = %s
		""", (str(id),)
	)
	post = cursor.fetchone()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
					  		detail=f"Post with id: {id} not found")
	return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
	cursor.execute(
		"""DELETE FROM posts 
		WHERE id = %s RETURNING *;""", (str(id),)
	)
	deleted_post = cursor.fetchone()
	conn.commit()
	if deleted_post is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
					  detail=f"Post with id {id} does not exit")

	return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int, post:Post):
	cursor.execute(
		"""UPDATE posts
		SET title = %s, content = %s, published = %s
		WHERE id = %s RETURNING *""", 
		(post.title, post.content, post.published, str(id))
	)
	updated_post = cursor.fetchone()
	conn.commit()
	if updated_post is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

	return {"updated": updated_post}
