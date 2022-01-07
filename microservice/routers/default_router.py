from fastapi import APIRouter, Response

model_router = APIRouter()
model_router.current_model = None

models = {
    "prosty": "model1",
    "zaawansowany": "model2"
}


def change_model(model_name):
    if model_name in models.keys():
        model_router.current_model = models[model_name]
        return True
    else:
        return False


@model_router.get("/models_names")
def model_names(response: Response):
    response.status_code = 201
    return {"models": list(models.keys())}


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
