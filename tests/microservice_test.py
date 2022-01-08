import pandas as pd


def create_input_for_microservie(session_id):
    test_df = pd.read_json(path_or_buf='data/processed/test_set.jsonl')
