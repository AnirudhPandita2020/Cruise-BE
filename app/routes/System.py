from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models import database, schemas, models
from sqlalchemy.orm import Session
from app.auth import oauth2
import time

router = APIRouter(prefix="/system", tags=["SYSTEM"])


@router.post("", status_code=status.HTTP_200_OK)
async def add_system(system: schemas.SystemCreate,
                     get_current_owner=Depends(oauth2.get_current_user),
                     db: Session = Depends(database.get_db)):
    get_sys = db.query(models.Systems).filter(models.Systems.name == system.name,
                                              models.Systems.ownerid == get_current_owner.id)

    if get_sys.first():
        return {
            "message": "System name :{} already present".format(system.name),
            "status": 0
        }

    new_system = models.Systems(**system.dict())
    new_system.in_user = False
    new_system.ownerid = get_current_owner.id

    db.add(new_system)
    db.commit()
    db.refresh(new_system)

    return {
        "message": "Added System {}".format(new_system.name),
        "status": 1
    }


def generateamount(end_time):
    time_spent = int(end_time)

    minutes = time_spent // 60;

    return 5 + minutes * 1


@router.get("", status_code=status.HTTP_200_OK, response_model=List[schemas.SystemList])
async def get_systems(db: Session = Depends(database.get_db),
                      get_current_owner: int = Depends(oauth2.get_current_user)):
    system_list = db.query(models.Systems).filter(models.Systems.ownerid == get_current_owner.id).all()

    return system_list


@router.put("{id}", status_code=status.HTTP_200_OK)
async def free_system(id: int, system: schemas.SystemCreate,
                      db: Session = Depends(database.get_db),
                      get_current_user: int = Depends(oauth2.get_current_user)):
    deallot_system = db.query(
        models.Systems
    ).filter(
        models.Systems.ownerid == get_current_user.id,
        models.Systems.id == id
    )

    if not deallot_system.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No system of id {} exist.".format(id))

    get_his = db.query(models.History).filter(models.History.ownerid == get_current_user.id,
                                              models.History.systemid == id).all()

    print(get_his[len(get_his) - 1].phone)

    time_data = db.query(models.User).filter(models.User.phone == get_his[len(get_his) - 1].phone)
    start_time = float(time_data.first().startTime)
    end_time = time.time() - start_time

    bill = generateamount(end_time)
    print(bill)

    set_end_time = schemas.setEndtime()

    set_end_time.endTime = str(end_time)

    time_data.update(set_end_time.dict(), synchronize_session=False);

    deallot_system.update(system.dict(), synchronize_session=False)
    db.commit()

    return {
        "message": "System is free",
        "bill": "{} is the total amount.Please pay at the counter".format(bill),
        "status": 0
    }
