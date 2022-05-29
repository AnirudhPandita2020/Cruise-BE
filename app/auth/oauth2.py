
from fastapi import Depends,HTTPException,status
from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models import models, schemas,database
from app.config.config import setting

#secret key
#specific alogorithm
#expiration time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes


def create_acess_token(payload:dict):
    data_to_encode = payload.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp":expire})
    
    encoded_jwt = jwt.encode(data_to_encode,SECRET_KEY,algorithm = ALGORITHM)
    
    return encoded_jwt


def verifytoken(token:str,exceptions):
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        id = payload.get("id")
        if id is None:
            raise exceptions
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise exceptions
    
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = "Credential Validation Failed",headers ={"WWW-Authenicate":"Bearer"})
    
    token = verifytoken(token,exceptions=exceptions)
    user = db.query(models.Owner).filter(models.Owner.id == token.id).first()
    
    return user
        
    
    
