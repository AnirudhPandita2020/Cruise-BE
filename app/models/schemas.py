from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from sqlalchemy import Column



class User(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    
    class Config:
        orm_mode = True
    

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str


class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    
    class Config:
        orm_mode = True
    
class Systems(BaseModel):
    id:int
    name:str
    added_at:datetime
    owner:User
    
    class Config:
        orm_mode = True
    
class SystemCreate(BaseModel):
    name:str
    
class SystemList(SystemCreate):
    class Config:
        orm_mode = True
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
    
    
class TokenData(BaseModel):
    id:Optional[str] = None