# schema definition for the request body wity pydantic
from typing import Optional
from pydantic import BaseModel, EmailStr, conint, StrictBool
from datetime import datetime



######### USER SCHEMAS #########
        
class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):  #avoid inheriting the password from UserBase
    #id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str



######### POST SCHEMAS #########
class PostBase(BaseModel):
    # id: int = None    # this would be handled by the database in a real scenario
    title: str
    content: str
    published: Optional[bool] = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


# schema definition for the response body with pydantic extending PostBase
class Post(PostBase):
    id: int
    user_id: int
    rating: Optional[int]
    created_at: datetime
    owner: UserResponse


    # this is to configure the response to be a dictionary
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


# OATH2 TOKEN SCHEMAS
class Token(BaseModel):
    access_token: str
    token_type: str
    # token_type: str = "bearer" 

class TokenData(BaseModel):
    id: Optional[int] = None



# VOTE SCHEMAS
class Vote(BaseModel):
    user_id: int
    post_id: int
    dir: conint(ge=0, le=1)   # type: ignore # direction of the vote can be 0 or 1
    
    class Config:
        from_attributes = True

class VoteResponse(BaseModel):
    user_id: int
    post_id: int

    class Config:
        from_attributes = True
