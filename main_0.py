from fastapi import FastAPI
from enum import Enum


class Level(str, Enum):
    easy = 'easy'
    medium = 'medium'
    advanced = 'advanced'

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


my_app = FastAPI()

@my_app.get("/home/{home_id}")
def home(home_id: int):
	return {"welcome_note": "Akwaaba", "id": home_id}

@my_app.get('/level/{level}/')
def level(level: Level):
	return {'name': level}

@my_app.get('/items/')
def get_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
