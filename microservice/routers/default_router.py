import pickle
from typing import Any

from fastapi import APIRouter, Response
from pydantic import BaseModel

from session_purchase.models.naive_model.NaiveModel import NaiveModel

model_router = APIRouter()
model_router.current_model = None
model_router.current_model_name = ""

naive_model = NaiveModel()
naive_model.load_model()

models = {
    "prosty": naive_model,
    "zaawansowany": "model2"
}


class InputData(BaseModel):
    session_id: int
    data: dict


def change_model(model_name):
    if model_name in models.keys():
        model_router.current_model = models[model_name]
        model_router.current_model_name = model_name
        return True
    else:
        return False


@model_router.get("/models_names")
def model_names(response: Response):
    response.status_code = 201
    return {"models": list(models.keys())}


@model_router.get("/current_model")
def model_names(response: Response):
    response.status_code = 201
    model_name = model_router.current_model_name
    if model_name is None:
        model_name = "none"
    return {"model_name": model_name}


@model_router.get("/")
def root():
    return {"message": "Hello model!"}


@model_router.get("/choose_model/{model_name}")
def choose_model(model_name: str, response: Response):
    if change_model(model_name):
        response.status_code = 201
        msg = f"Model changed to {model_name}"
    else:
        response.status_code = 403
        msg = f"Name of model not found!"
    return {"result": msg}


@model_router.post("/predict")
def perform_prediction(response: Response, input_data: InputData):
    response.status_code = 201
    prediction = model_router.current_model.predict_model(input_data.data)
    return {'prediction:': prediction}

