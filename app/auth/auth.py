import imp
from fastapi import HTTPException,status,APIRouter,Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.models import database,models,schemas
from app.utils import utils
from sqlalchemy.orm import Session
from app.auth import oauth2

router = APIRouter(prefix="/login",tags=["Authetication"])

@router.post("/")
def login(user_cred:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):
    user = db.query(models.Owner).filter(models.Owner.email == user_cred.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Creds")
    
    if not utils.verify(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Creds")
    
    access_token = oauth2.create_acess_token(payload = {"id":user.id})
    
    return {"access_token":access_token,"token_type":"bearer","userid":user.id,"email":user.email,"username":user.username}