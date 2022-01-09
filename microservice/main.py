from logging.config import dictConfig

from fastapi import FastAPI, Request
from microservice.routers.default_router import model_router
import uvicorn
import logging
from config.LogConfig import LogConfig

app = FastAPI()

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")
app.include_router(model_router, prefix="/model", tags=["default", "file"])


@app.get("/")
def root():
    return {"wiadomosc": "Witam projekt IUM!"}


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("microservice.main:app", host="0.0.0.0", port=2115, reload=True)
