from app.models import database, models
from sqlalchemy.orm import Session
from app.models import schemas
from app.auth import oauth2
from fastapi import APIRouter, Depends, HTTPException, status
import time

router = APIRouter(prefix="/users", tags=["USER"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_user(user: schemas.UserAdd,
                   db: Session = Depends(database.get_db),
                   get_current_owner: int = Depends(oauth2.get_current_user)):
    if db.query(
            models.User
    ).filter(
        models.User.phone == user.phone
    ).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "message": "User is already occupied",
            "status": 1
        })
    if not db.query(
            models.Systems
    ).filter(
        models.Systems.in_user == False,
        models.Systems.id == user.system_id
    ).first():
        return {
            "message": "System is busy",
            "status": 1
        }

    new_user = models.User(**user.dict())
    new_user.startTime = str(time.time())
    new_user.endTime = "0"
    system_to_allot = db.query(
        models.Systems
    ).filter(
        models.Systems.id == new_user.system_id,
        models.Systems.ownerid == get_current_owner.id
    )

    is_already_full = db.query(
        models.Systems
    ).filter(
        models.Systems.in_user == False,
        models.Systems.id == user.system_id
    )

    if not system_to_allot.first():
        message = {
            "message": "System does not exist",
            "status": 1
        }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    if not is_already_full.first():
        raise HTTPException(status_code=status.HTTP_200_OK, detail={
            "message": "System is occupied",
            "status": 1
        })

    sys_update = schemas.System_update()
    sys_update.in_user = True

    system_to_allot.update(sys_update.dict(), synchronize_session=False)
    db.commit()

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    add_history = models.History()

    add_history.systemid = user.system_id
    add_history.phone = user.phone
    add_history.name = user.name
    add_history.ownerid = get_current_owner.id

    db.add(add_history)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Added user to System id {}".format(user.system_id),
        "status": "active"
    }
