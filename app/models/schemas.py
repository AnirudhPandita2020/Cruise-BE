from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from sqlalchemy import Column



class OwnerCreate(BaseModel):
    username:str
    email:EmailStr
    password:str

class Owner(BaseModel):
    id:int
    username:str
    email:str
    created_at:datetime
    class Config:
        orm_mode = True

class SystemList(BaseModel):
    id:int
    name:str
    added_at:datetime
    ownerid:int
    in_user:bool
    owner:Owner
    
    class Config:
        orm_mode = True
        
class SystemCreate(BaseModel):
    name:str
    in_user:Optional[bool] =False
    
class UserAdd(BaseModel):
    name:str
    phone:str
    system_id:int
    
class History(BaseModel):
    name:str
    system_id:int
    class Config:
        orm_mode = True
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str] = None
    

class System_update(BaseModel):
    in_user:Optional[bool] = False