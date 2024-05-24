from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List


from .. import models, schemas, utils
from ..database import get_db


# create the router for fastAPI to the app in main
router = APIRouter(
    prefix="/users", tags=["users"]
)  # create a router for the users


# create a new user via post request
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)) -> dict:
    '''create a new user and return it as a dictionary'''
    # hash the password
    user.password = utils.hash_password(user.password)
    
    new_user = models.User(**user.model_dump())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Could not create this new user. Make sure {user.email} doesn't already exists"         
        )

    return new_user


# get all users
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)) -> List[dict]:
    '''get all users from db.[users] and return them as a list of dictionaries'''
    all_users = db.query(models.User).all()
    return all_users


# get user by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Session=Depends(get_db)) -> dict:
    '''get a user by id and return it as a dictionary'''
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {id} not found"         
        )
    return user

