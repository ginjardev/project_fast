from fastapi import FastAPI, Body, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
	id: Optional[int] = None
	title: str
	content: str
	published: bool = True
	rating: Optional[int] = None

posts_list = []

def find_post(id:int):
	for p in posts_list:
		if p['id'] == id:
			return p


def find_post_index(id):
	for i , p in enumerate(posts_list):
		if id == p['id']:
			return i



@app.get("/post")
async def posts():
	return {"posts": posts_list}

@app.post('/post', status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
	post.id = randrange(0, 1001)
	post.rating = randrange(1,6)
	post_dict = post.model_dump()
	posts_list.append(post_dict)
	return {"post": post_dict}

@app.get("/posts/{id}")
def get_post(id:int):
	post = find_post(id)
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
					  		detail=f"Post with id: {id} not found")
	return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
	index = find_post_index(id)
	if index is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
					  detail=f"Post with id {id} not found")
	posts_list.pop(index)

	return Response(status_code=status.HTTP_204_NO_CONTENT)