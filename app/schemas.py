#here we define what a responce shuld look like

from pydantic import BaseModel,EmailStr #to specify what a pos or a request shuld look like
from datetime import datetime
from typing import Optional, Annotated
from pydantic.types import conint



class PostBase(BaseModel):#based on this model the api will check if the request have the body we want
    title: str
    content: str 
    published: bool = True



class PostCreate(PostBase):#because the user will only update the certain field, for creating a post
    pass

class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

#defining the structure of a responce
class Post(PostBase):
    id:int
    created_at: datetime
    owner_id: int #حطيناه هنا عشان اليوزر مايضطر لتوفير الايدي وهذا السكيما يعطي اليوزر ماياخذ
    owner: UserOut


    class Config:
        from_attributes = True

#for creating users
class UserCreate(BaseModel):
    email: EmailStr
    password: str 



#for JWT
#to ensure the logging info
class UserLogin(BaseModel):
    email: EmailStr
    password: str 


#schema for tokens

class Token(BaseModel):
    access_token: str 
    token_type: str 

#token data
class TokenData(BaseModel):
    id: Optional[str]=None

#schema for votingon
class Vote(BaseModel):
    post_id: int 
    dir: Annotated[int,conint(ge=0,le=1)]

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True