import session_purchase.models.random_forest.predict_model
import session_purchase.models.neural_network.predict_model
import numpy as np


def test_neural_network_predict():
    random_data = [5.0, 19.0, 1000.98, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 2.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 1.0, 7.0, 28.0, 15.0, 2.0]
    prediction = session_purchase.models.neural_network.predict_model.predict(random_data)
    assert (type(prediction) == np.float32)
    assert (prediction >= 0.0)
    assert (prediction <= 1.0)


def test_random_forest_predict():
    random_data = [5.0, 19.0, 1000.98, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 2.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 1.0, 7.0, 28.0, 15.0, 2.0]
    prediction = session_purchase.models.random_forest.predict_model.predict(random_data)
    assert (type(prediction) == np.float64)
    assert (prediction >= 0.0)
    assert (prediction <= 1.0)
