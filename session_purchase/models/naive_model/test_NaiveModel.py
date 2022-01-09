import os

import pandas as pd
import pytest
from .NaiveModel import NaiveModel, OUT_FILE_PATH


def test_create():
    model = NaiveModel()
    assert model is not None
    assert model.treshold is None


def test_trainmodel():
    os.remove(OUT_FILE_PATH)
    assert not os.path.isfile(OUT_FILE_PATH)
    model = NaiveModel()
    model.train_model()
    assert os.path.isfile(OUT_FILE_PATH)


def test_loadmodel():
    model = NaiveModel()
    assert model.treshold is None
    model.load_model()
    assert model.treshold is not None


def test_predictmodel():
    # assuming that model wont return only 0 or 1
    df_train = pd.read_json(path_or_buf='data/processed/train_set.jsonl')
    min_len = df_train['session_length'].min()
    max_len = df_train['session_length'].max()
    simple_data_min = [5 for _ in range(38)]
    simple_data_max = [5 for _ in range(38)]
    simple_data_min[32] = 0
    simple_data_max[32] = max_len
    model = NaiveModel()
    model.load_model()
    assert model.predict_model(simple_data_min) == 0
    assert model.predict_model(simple_data_max) == 1
