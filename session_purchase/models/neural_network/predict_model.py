import keras.models
import numpy as np


def predict(x):
    model = keras.models.load_model('models/nn')
    return model.predict(np.array(x, dtype=np.float64).reshape(1, -1))[0][0]
