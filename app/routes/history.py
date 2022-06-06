from copy import deepcopy
from pyexpat import model
from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from sqlalchemy.orm import Session
from app.auth import oauth2
from app.models import models,database,schemas


router = APIRouter(prefix="/history",tags=["History"])

@router.get("",status_code=status.HTTP_200_OK,response_model=List[schemas.History])
async def get_History(db:Session = Depends(database.get_db),get_current_owner:int = Depends(oauth2.get_current_user)):
    get = db.query(models.History).filter(models.History.ownerid == get_current_owner.id).all()
    return get
    