#utility fubctions
from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")#hashing the password in the database

def hash(password: str):
    return pwd_context.hash(password)

#for comparing the passwords of the user
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)