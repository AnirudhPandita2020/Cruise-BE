from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, System, history, owner
from app.auth import auth

description = """
[ base url : http://127.0.0.1:8000/ ]
"""

app = FastAPI(
    title="Cruise",
    description=description,
    version="1.0.1",
    contact={
        "name": "Anirudh Pandita",
        "url": "https://www.linkedin.com/in/anirudh-pandita-a0b532200/",
        "email": "kppkanu@gmail.com",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(System.router)
app.include_router(history.router)
app.include_router(owner.router)


@app.get("/",include_in_schema=False)
async def root():
    return {"Message": "Type /docs in endpoint"}
