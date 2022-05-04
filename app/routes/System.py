import imp
from msilib import schema
from fastapi import APIRouter,Depends,HTTPException,Response,status
from typing import List
from app.models import database,schemas,models
from sqlalchemy.orm import Session
from app.auth import oauth2

router = APIRouter(prefix="/system",tags = ["SYSTEM"])

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.Systems])
async def get_Systems(db:Session = Depends(database.get_db),user_id:int = Depends(oauth2.get_current_user)):
    sys_list = db.query(models.Systems).filter(models.Systems.ownerid == user_id.id).all()
    return sys_list

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Systems)
async def create_system(data:schemas.SystemCreate,db:Session = Depends(database.get_db),user_id:int = Depends(oauth2.get_current_user)):
    new_sys = models.Systems(**data.dict())
    new_sys.ownerid = user_id.id
    db.add(new_sys)
    db.commit()
    db.refresh(new_sys)
    return new_sys