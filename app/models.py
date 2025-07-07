#create the database tables
#Note, we cannot modify the table once its made, if we want, we can delete it and refresh 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
#create a model for post
class Post(Base):
    __tablename__="posts"#table name

    #define the columns
    id=Column(Integer, primary_key=True,nullable=False)
    title=Column(String, nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='TRUE',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")#when we retreive a post its going to retutn the owner property based on the relationship to the user



#table for users
class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    #if we want to add a column, just add it here and then type alembic autogenerate -m "jisjjs", and them alembic upgrade head, and it will add it to postgres!!


class Vote(Base):
    __tablename__="votes"
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    
#Note, we cannot modify the table once its made, if we want, we can delete it and refresh 