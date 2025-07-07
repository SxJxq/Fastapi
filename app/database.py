#database codes

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor# to know the colmns because the default results doens contain it
import time
from .config import settings

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'#connection string

#create angine to connect
engine=create_engine(SQLALCHEMY_DATABASE_URL)

#to talk to the database
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

#dependency for getting a session for the database
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()




##code to connecting to the database manwally but we dont need it since we have sqlalchemy
#while True:#while loop because we wont start the api app until the connection to the database is successful
##DATABASE PART
    #try:
        #conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='7364',cursor_factory=RealDictCursor)
        #cursor=conn.cursor()#using this to execute sql statements
        #print("connection successful")
        #break
    #except Exception as error:
        #print("connection failed")
        #print("error:",error)
        #time.sleep(2)#wait before trying to reconnect