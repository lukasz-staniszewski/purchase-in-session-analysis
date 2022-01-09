import datetime
import pickle
from logging.config import dictConfig
from typing import Any
import logging
import pandas as pd
from fastapi import APIRouter, Response
from pydantic import BaseModel

import session_purchase.models.random_forest.predict_model
import session_purchase.models.neural_network.predict_model
from config.LogConfig import LogConfig
from session_purchase.models.naive_model.NaiveModel import NaiveModel

model_router = APIRouter()
model_router.current_model = None
model_router.current_model_name = ""

dictConfig(LogConfig().dict())
model_router.logger = logging.getLogger("mycoolapp")

naive_model = NaiveModel()
naive_model.load_model()

ab_logs_file = "logs/ab_predictions.csv"

models = {
    "naive": naive_model.predict_model,
    "random_forest": session_purchase.models.random_forest.predict_model.predict,
    "nn": session_purchase.models.neural_network.predict_model.predict
}


class PredictData(BaseModel):
    data: list


class ABData(BaseModel):
    session_id: int
    data: list


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
        model_router.logger.info(msg)
    else:
        response.status_code = 403
        msg = f"Name of model not found!"
        model_router.logger.warning(msg)
    return {"result": msg}


@model_router.post("/predict")
def perform_prediction(response: Response, input_data: PredictData):
    if len(input_data.data) != 38:
        response.status_code = 404
        model_router.logger.warning(f"Bad input length {len(input_data.data)} - should be 38")
        return {'msg': 'Input data should be in length 38!'}
    response.status_code = 201
    prediction = models[model_router.current_model_name](input_data.data)
    model_router.logger.info(f"Model: {model_router.current_model_name} Predicted: {prediction} input_data: {input_data.data}")
    return {'prediction:': float(prediction)}


@model_router.post("/ab/reset_ab")
def reset_ab(response: Response):
    response.status_code = 201
    with open(ab_logs_file, 'w') as file:
        file.write('session_id;model_name;prediction;timestamp\n')
    return {'msg': 'Reset of AB predictions file performed!'}


@model_router.post("/ab/add_sample")
def add_sample(response: Response, input_data: ABData):
    if len(input_data.data) != 38:
        response.status_code = 404
        return {'msg': 'Input data should be in length 38!'}
    if input_data.session_id % 2 == 0:
        model_name = 'random_forest'
    else:
        model_name = 'naive'
    prediction = models[model_name](input_data.data)
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(ab_logs_file, 'a') as file:
        file.write(f"{input_data.session_id};{model_name};{prediction};{current_time}\n")
    response.status_code = 201
    return {"model_name": model_name, "prediction": prediction}


@model_router.post("/ab/perform_ab")
def perform_ab(response: Response):
    df = pd.read_csv(ab_logs_file, delimiter=';')
    print(df)
