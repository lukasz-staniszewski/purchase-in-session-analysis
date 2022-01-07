from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from microservice.routers.default_router import model_router
import uvicorn

app = FastAPI()
app.include_router(model_router, prefix="/model", tags=["default"])


@app.get("/")
def root():
    return {"wiadomosc": "Witam projekt IUM!"}


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("microservice.main:app", host="0.0.0.0", port=2115, reload=True)
