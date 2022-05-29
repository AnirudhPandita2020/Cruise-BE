from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from sqlalchemy.orm import Session
from app.auth import oauth2
from app.utils import utils
from app.models import models,database,schemas


router = APIRouter(prefix="/owner",tags=["Owner"])

@router.post("",status_code=status.HTTP_201_CREATED)
async def add_owner(owner:schemas.OwnerCreate,
                    db:Session = Depends(database.get_db)):
    
    
    exists_owner = db.query(models.Owner).filter(
        models.Owner.email == owner.email
    ).first()
    
    if exists_owner:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Owner is already present")
    
    owner.password = utils.hash(owner.password)
    new_owner = models.Owner(**owner.dict())
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    
    return {
        "message":"Owner added",
        "status":0
    }
    