from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from sqlalchemy.orm import Session
from app.auth import oauth2
from app.models import models,database,schemas


router = APIRouter(prefix="/history",tags=["History"])