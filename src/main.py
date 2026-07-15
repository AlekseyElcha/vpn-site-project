from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.v1.inbounds import router as inbounds_router

load_dotenv()
app = FastAPI()

app.include_router(router=inbounds_router)

@app.get("/")
async def root():
    return {
        "msg": "working"
    }