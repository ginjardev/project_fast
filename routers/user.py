from fastapi import status, HTTPException, Depends, APIRouter
from schemas import UserCreate, UserOut
from models import User
from database import get_db
from sqlalchemy.orm import Session
import models, utils


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(id:int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )
    return user
