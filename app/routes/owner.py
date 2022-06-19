from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.utils import utils
from app.models import models, database, schemas

router = APIRouter(prefix="/owner", tags=["Owner"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_owner(owner: schemas.OwnerCreate,
                    db: Session = Depends(database.get_db)):
    exists_owner = db.query(models.Owner).filter(
        models.Owner.email == owner.email
    ).first()

    if exists_owner:
        return {
            "message": "Owner already present",
            "status": 1
        }

    owner.password = utils.hash(owner.password)
    new_owner = models.Owner(**owner.dict())
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)

    return {
        "message": "Owner added",
        "status": 0
    }
