#all other files will automatically import this
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest
from app.oauth2 import create_access_token
from app import models


#SQLALCHEMY_DATABASE_URL='postgresql://postgres:7364@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'#connection string

#create angine to connect
engine=create_engine(SQLALCHEMY_DATABASE_URL)

#to talk to the database
TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine) #this what allows us to query the DATABASE












#client = TestClient(app) #everytime we use client its going to refer to the new database, usi it to ganerates the request
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)#command.downgrade("head") to solve the issue where we have to delete the users before4 we run our tests
    Base.metadata.create_all(bind=engine)#command.upgrade("head")
    db=TestingSessionLocal()
    try:
        yield db#database object we use to query things
    finally:
        db.close()




@pytest.fixture()#function that runs beforw the tests
def client(session):# it will run the session fixture before it runs, This client is a special tool that:
#Acts like a browser or API client.
#Simulates real HTTP requests to your FastAPI app — without actually starting a server.

    def override_get_db():
        try:
            yield session 
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db 
    #run the code before we run our test
    yield TestClient(app)#returning the test client instance
    #run the code after the test finishes

#another user 
@pytest.fixture
def test_user2(client):
    user_data = {"email": "soso123@gmail.com", "password":"123"}
    res=client.post("/users/", json=user_data)#Sends a real POST request to /users/ to create a user.

    assert res.status_code == 201

    new_user=res.json()
    new_user['password'] = user_data['password']
    return new_user


#original user
@pytest.fixture
def test_user(client):
    user_data = {"email": "soso@gmail.com", "password":"123"}
    res=client.post("/users/", json=user_data)#Sends a real POST request to /users/ to create a user.

    assert res.status_code == 201

    new_user=res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):#to give us an authonticated client instead of the regular client
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client


#posts so we can perform our tests on 
@pytest.fixture
def test_posts(test_user, session, test_user2):#no post without a user, we will connect to the database so session in important
    posts_data= [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    },
    {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
    {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
    {
        "title": "4rd title",
        "content": "4rd content",
        "owner_id": test_user2['id']
    }]


    #how to convert the dictionary to this format
    def create_user_model(post):
        return models.Post(**post)#** means spread it, title=kdkd, content= ...etc
    post_map=map(create_user_model, posts_data)#create_user_model will take each item in posts_data and convert it to models.post
    posts=list(post_map)#convert it to a list
    session.add_all(posts)


    #create new user model
    #session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']),models.Post(title="3nd title", content="3nd content", owner_id=test_user['id']) ])
    session.commit()
    posts=session.query(models.Post).all()
    return posts