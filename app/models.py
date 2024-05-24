from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    content = Column(String,  nullable=False)
    published = Column(Boolean, default=True)
    rating = Column(Integer, nullable=True, server_default=null())
    created_at = Column(TIMESTAMP(timezone='TRUE'), 
                        server_default=text('now()'), nullable=False)
    
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone='TRUE'), 
                        server_default=text('now()'), nullable=False)
    

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    
    