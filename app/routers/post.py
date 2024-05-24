from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from .. import models, schemas, utils, oauth2
from ..database import get_db



# create the router for fastAPI to the app in main
router = APIRouter(
    prefix="/posts", tags=["posts"]
) 


# methods for the API - order matters "posts/latest" should be before "posts/{id}" due to paths matching

# get all posts
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              limit: int=10,
              skip: int=0,
              search: Optional[str]="") -> List[dict]:
    
    '''get all posts from db.[posts] and return them as a list of dictionaries'''
    
    result = db.query(
        models.Post, func.count(models.Vote.post_id).label('votes')) \
            .join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True) \
            .group_by(models.Post.id) \
            .filter(
                models.Post.title.contains(search) | models.Post.content.contains(search)
            ).limit(limit).offset(skip).all()

    return result


# get one post by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
def get_post(id: int, 
             db: Session=Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user) ) -> dict:
    
    '''get a post by id and return it as a dictionary'''

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')) \
                    .join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True) \
                    .filter(models.Post.id == id) \
                    .group_by(models.Post.id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} not found"         
        )
    # check if user is the owner of the post
    if post.Post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {current_user.email} is not the owner of post {id}"         
        )
    
    return post

# create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate,
                db: Session=Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)) -> dict:
    
    '''create a new post and return it as a dictionary'''

    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# delte post - 204 delete doesn't return any content by default in FastAPI
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                 db: Session=Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)) -> Response:
    '''delete a post by id and return a 204 status code'''
    # check if post exists
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if not post_query.first():   # if not raise 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} not found"         
        )
    
    # check if user is the owner of the post
    if post_query.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {current_user.email} is not the owner of post {id}"         
        )
    
    # delete post
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a post by id
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostUpdate, 
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)) -> dict:
    query = db.query(models.Post).filter(models.Post.id == id)
    
    if query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} not found"         
        )
    
    # check if user is the owner of the post
    if query.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {current_user.email} is not the owner of post {id}"         
        )
    
    post_dict = post.model_dump()
    if "id" in post_dict:
        del post_dict["id"]

    query.update(post_dict, synchronize_session=False)
    db.commit()
    print(type({"updated_post": query.first()}))
    return query.first()  # return the updated post by running the query again
