from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"Message":"Type /docs in endpoint"}