#setting up a new VE
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user , auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine) #we dont need it sense we have olembic

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,#a function that runs before any request
    allow_origins=origins,#domains that our api is able to talk to
    allow_credentials=True,
    allow_methods=["*"],#allow specific http methods, like post and delete
    allow_headers=["*"],# -- 
)

app.include_router(post.router)#instead of all the path operations
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "lak sho hayda al7akiii"}


