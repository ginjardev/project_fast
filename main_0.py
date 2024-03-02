from fastapi import FastAPI
from enum import Enum


class Level(str, Enum):
	easy = 'Easy'
	medium = 'Medium'
	advanced = 'Advanced'

my_app = FastAPI()

@my_app.get("/home/{home_id}")
def home(home_id: int):
	return {"welcome_note": "Akwaaba", "id": home_id}

@my_app.get('/level/{level}')
def level(level: Level):
	return {'name': level}