import pickle
import numpy as np


def predict(x):
    model = pickle.load(open("models/random_forest/random_forest.sav", "rb"))
    return model.predict(np.array(x).reshape(1, -1))[0]
