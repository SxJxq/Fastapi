from .. import models, schemas, oauth2
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from typing import Optional
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func


router=APIRouter(
    prefix="/posts",#so we dont have to write /posts in every path
    tags=['Posts']# to group it in the documentation
)#to replace the keyword (app)



#GET POSTS
@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user), limit: int = 10, skip: int=0, search: Optional[str]=""):#limit is for letting the user filter the posts, depending on the query parameters
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    #print(limit)
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

#CREATE POST
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):#extract body fields in the request and convert them into dictionary, here we get a post from the front end so we have to make sure there in the right structure, we get the access token and verify its good to perform a logic that requers the user to be logged in
    #cursor.execute("""INSERT INTO posts (title, content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))#for sql ingections
    #new_post=cursor.fetchone()#the returned sql result
    #conn.commit()#push the changes into postgresql 
    
    new_post=models.Post(owner_id=current_user.id ,**post.model_dump())#it was title=post.title,content=post.content,published=post.published instead of **post.dict()
    db.add(new_post)#add to the database
    db.commit()
    db.refresh(new_post)#same as RETURNING
    return new_post


#RETRIEVE ONE POST
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):#the (:int) part is for validait that the id  can br converted ti an integer and then automatically convert it 
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    #post=cursor.fetchone()

    #post=db.query(models.Post).filter(models.Post.id==id).first()#filter is like WHERE in sql

    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()#filter is like WHERE in sql

    if not post:#if we didnt find the post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")#so that the frontend knows that the post doesnt exsist
    return post


#DELETING A POST
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),))
    #deleted_post=cursor.fetchone()
    #conn.commit()




    post_query=db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesnt exist")
    
    if post.owner_id != current_user.id:# to make sure a user is deleting their own post, not other user`s post
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized toperform the requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



#UPDATE POSTS
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):#here we get a post from the front end so we have to make sure there in the right structure
    #cursor.execute("""UPDATE posts SET title=%s , content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()


    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesnt exist")
    
    if post.owner_id != current_user.id:# to make sure a user is deleting their own post, not other user`s post
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized toperform the requested action")
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()
