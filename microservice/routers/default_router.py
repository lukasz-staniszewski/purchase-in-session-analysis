import datetime
import pickle
from typing import Any

import pandas as pd
from fastapi import APIRouter, Response
from pydantic import BaseModel

import session_purchase.models.random_forest.predict_model
import session_purchase.models.neural_network.predict_model
from session_purchase.models.naive_model.NaiveModel import NaiveModel

model_router = APIRouter()
model_router.current_model = None
model_router.current_model_name = ""

naive_model = NaiveModel()
naive_model.load_model()

ab_logs_file = "logs/ab_predictions.csv"

models = {
    "naive": naive_model.predict_model,
    "random_forest": session_purchase.models.random_forest.predict_model.predict,
    "nn": session_purchase.models.neural_network.predict_model.predict
}


class InputData(BaseModel):
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
        msg = f"Model changed to {model_router.current_model_name}"
    else:
        response.status_code = 403
        msg = f"Name of model not found!"
    return {"result": msg}


@model_router.post("/predict")
def perform_prediction(response: Response, input_data: InputData):
    if model_router.current_model_name == "":
        response.status_code = 403
        return {'msg': 'You have to choose model!'}
    if len(input_data.data) != 38:
        response.status_code = 404
        return {'msg': 'Input data should be in length 38!'}
    response.status_code = 201
    prediction = models[model_router.current_model_name](input_data.data)
    return {'prediction:': float(prediction)}


@model_router.post("/ab/reset_ab")
def reset_ab(response: Response):
    response.status_code = 201
    with open(ab_logs_file, 'w') as file:
        file.write('session_id;model_name;prediction;timestamp\n')
    return {'msg': 'Reset of AB predictions file performed!'}


@model_router.post("/ab/add_sample")
def add_sample(response: Response, input_data: InputData):
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
    ab_df = pd.read_csv(ab_logs_file, delimiter=';')
    if ab_df.shape[0] < 2 or ab_df.loc[ab_df['model_name'] == 'random_forest'].shape[0] < 1 or \
            ab_df.loc[ab_df['model_name'] == 'naive'].shape[0] < 1:
        response.status_code = 403
        return {"msg": "A/B logs file is not ready to perform A/B test!"}
    models_accuracy = {
        'naive': {
            'positives': 0,
            'all': 0,
        },
        'random_forest': {
            'positives': 0,
            'all': 0,
        }
    }
    test_data = pd.read_json(path_or_buf='data/processed/test_set.jsonl')
    for row in ab_df.values:
        set_row = test_data.loc[test_data['session_id'] == row[0]]
        if set_row.shape[0] == 0:
            response.status_code = 403
            return {"msg": "A/B logs file contains session_id that is not in test set, consider adding it or resetting "
                           "A/B test!"}
        else:
            if int(set_row['purchased'].values[0]) == int(row[2] > 0.5):
                models_accuracy[row[1]]['positives'] += 1
            models_accuracy[row[1]]['all'] += 1
    response.status_code = 201
    return {
        "Naive accuracy on A/B test:": f"{models_accuracy['naive']['positives'] / models_accuracy['naive']['all'] * 100:.3f}%",
        "Random forest accuracy on A/B test:": f"{models_accuracy['random_forest']['positives'] / models_accuracy['random_forest']['all'] * 100:.3f}%"
    }
