import os

import pandas as pd


def create_input_for_microservice(session_id):
    test_df = pd.read_json(path_or_buf='../data/processed/test_set.jsonl')
    if session_id not in list(test_df['session_id']):
        print("There is no record in set that satisfy given session_id!")
        return False
    row = test_df.loc[test_df['session_id'] == session_id]
    row.drop(columns=['session_id', 'purchased'], inplace=True)
    return {"session_id": session_id,
            "data": row.values.tolist()[0]}


if __name__ == '__main__':
    print(create_input_for_microservice(8826))
