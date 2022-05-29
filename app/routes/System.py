from copy import deepcopy
import imp
from msilib import schema
from unittest import async_case
from fastapi import APIRouter,Depends,HTTPException,Response,status
from typing import List
from app.models import database,schemas,models
from sqlalchemy.orm import Session
from app.auth import oauth2

router = APIRouter(prefix="/system",tags = ["SYSTEM"])


@router.post("",status_code=status.HTTP_201_CREATED)
async def add_system(system:schemas.SystemCreate,
                     get_current_owner:int =Depends(oauth2.get_current_user),
                     db:Session = Depends(database.get_db)):
    
    new_system = models.Systems(**system.dict())
    new_system.in_user = 0
    new_system.ownerid = get_current_owner.id
    
    db.add(new_system)
    db.commit()
    db.refresh(new_system)
    
    return {
        "message":"Added System {}".format(new_system.name),
        "status":0
    }    
    
@router.get("",status_code= status.HTTP_200_OK,response_model=List[schemas.SystemList])
async def get_systems(db:Session = Depends(database.get_db),
                      get_current_owner :int = Depends(oauth2.get_current_user)):
    
    system_list = db.query(models.Systems).filter(models.Systems.ownerid == get_current_owner.id).all()
    
    return system_list

@router.put("{id}",status_code=status.HTTP_200_OK)
async def free_system(id:int,system:schemas.SystemCreate,
                      db:Session = Depends(database.get_db),
                      get_current_user:int = Depends(oauth2.get_current_user)):
    
    deallot_system = db.query(
        models.Systems
    ).filter(
        models.Systems.ownerid == get_current_user.id,
        models.Systems.id == id
    )
    
    if not deallot_system.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="No system of id {} exist.".format(id))
    
    deallot_system.update(system.dict(),synchronize_session=False)
    db.commit()
    
    return {
        "message":"System is free",
        "status":0
    }