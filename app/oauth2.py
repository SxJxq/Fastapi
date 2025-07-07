from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')#end point of logging in 


#secret key
SECTER_KEY = settings.secret_key
ALGORITHM = settings.algorithm#algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes#expriation time



def create_access_token(data: dict):

    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode=data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt=jwt.encode(to_encode, SECTER_KEY, algorithm=ALGORITHM)
    return encoded_jwt


#verify the access token
def verify_access_token(token: str, credentials_exception):
    try:
        payload=jwt.decode(token, SECTER_KEY, algorithms=ALGORITHM)#payload data

        #to extract payload data
        id:str= payload.get("user_id")

        if id is None:
            raise credentials_exception
    
        token_data=schemas.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(database.get_db)):
    credentials_excepteion=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})


    token = verify_access_token(token, credentials_excepteion)
    user = db.query(models.User).filter(models.User.id == token.id).first()#fetch the user from the database


    return user



