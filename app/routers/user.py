#CREATING A USER
from .. import models, schemas,utils
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router=APIRouter(
    prefix="/users",
    tags=['Users']
)#to replace the keyword (app)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session=Depends(get_db)):
    
    #hash the password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user=models.User(**user.model_dump())#it was title=post.title,content=post.content,published=post.published instead of **post.dict()
    db.add(new_user)#add to the database
    db.commit()
    db.refresh(new_user)#same as RETURNING
    return new_user

#RETREIVE INFO BASED ON USER ID
@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int, db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} doesnt exist")
    return user 

