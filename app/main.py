
import imp
from operator import mod
from fastapi import FastAPI
from .routes import user,System,history,owner
from app.auth import auth
from  app.models.database import engine
from app.models import models

app = FastAPI()



app.include_router(user.router)
app.include_router(auth.router)
app.include_router(System.router)
app.include_router(history.router)
app.include_router(owner.router)
@app.get("/")
async def root():
    return {"Message":"Type /docs in endpoint"}
