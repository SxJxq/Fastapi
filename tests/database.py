#WE DONT NEED THIS FILE





from fastapi.testclient import TestClient#Why: This gives you the TestClient, which simulates real HTTP requests (.get(), .post(), etc.) to your FastAPI app without running a server.
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base#get_db: The dependency that returns a DB session in your app. You override it in tests.Base: Used to create/drop tables in the test DB during setup/teardown.


import pytest


#SQLALCHEMY_DATABASE_URL='postgresql://postgres:7364@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'#connection string

#create angine to connect
engine=create_engine(SQLALCHEMY_DATABASE_URL)#This actually creates a connection engine for SQLAlchemy to talk to the test DB.

#to talk to the database
TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine) #this what allows us to query the DATABASE



















