from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List


from .. import models, schemas, utils, oauth2
from ..database import get_db


# create the router for fastAPI to the app in main
router = APIRouter(
    prefix="/votes", tags=["votes"]
)  # create a router for the users


# create a new vote via post request
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote, 
                db: Session=Depends(get_db),
                current_user: int=Depends(oauth2.get_current_user) ) :
    
    '''create a new vote and return it as a dictionary'''

    # check if the post exists at all
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {vote.post_id} not found"         
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == vote.user_id,
        models.Vote.post_id == vote.post_id
    )
    vote_found = vote_query.first()
    
    # logic for adding a vote
    if vote.dir == 1:
        # if the vote already exists in db, raise an error
        if vote_found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vote for user {vote.user_id} and post {vote.post_id} already exists"         
            )
        # if the vote is not found, create a new vote
        else:
            # remove the dir attribute from the vote object as it's not in the model
            del vote.dir  
            new_vote = models.Vote(**vote.model_dump())
            try:
                db.add(new_vote)
                db.commit()
                db.refresh(new_vote)
                return f"new vote added for {new_vote.user_id} and {new_vote.post_id}"
            except:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Could not create this new vote. Please try again"         
                )
            
    # logic for deleting a vote
    if vote.dir == 0:
        # if the vote is not found, delete it from the db
        if vote_found:
            vote_query.delete()
            db.commit()
            return f"deleted vote for {vote.user_id} and {vote_found.post_id}"
        # if the vote is not found, raise an error
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote {vote.user_id} and {vote.post_id} not found"         
            )
        


