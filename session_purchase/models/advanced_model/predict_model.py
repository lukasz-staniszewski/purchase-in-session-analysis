import keras.models
import numpy as np


def predict(x):
    model = keras.models.load_model('../../models/trained_model')
    return model.predict(np.array(x, dtype=np.float64)) > 0.5
