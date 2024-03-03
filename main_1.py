from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Annotated

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None

app = FastAPI()


@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
