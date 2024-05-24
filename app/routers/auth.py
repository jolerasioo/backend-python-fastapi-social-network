from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2




router = APIRouter(
    tags=["auth"]
)  # create a router for the auth

# login
@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token) 
def login(
    user_creds: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> dict:
    '''login a user and return a JWT token'''
    user = db.query(models.User).filter(
        models.User.email == user_creds.username
        ).first()
    
    if not user or not utils.verify_password(user_creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials."
        )
    
    payload = {"user_id": user.id}
    token = oauth2.create_access_token(payload)

    return {"access_token": token, "token_type": "bearer"}