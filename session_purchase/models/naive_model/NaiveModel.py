import pickle

import pandas as pd

OUT_FILE_PATH = 'models/naive_model/simple_treshold.txt'


class NaiveModel:
    def __init__(self):
        self.treshold = None

    def load_model(self):
        with open(OUT_FILE_PATH, "rb") as file:
            self.treshold = pickle.loads(file.read())

    def train_model(self):
        df_train = pd.read_json(path_or_buf='data/processed/train_set.jsonl')
        max_accuracy = -1
        best_threshold = -1
        for n_seconds in range(df_train['session_length'].min(), df_train['session_length'].max()):
            naive_predictions = df_train['session_length'] >= n_seconds
            current_accuracy = (naive_predictions == df_train['purchased'].to_numpy()).sum() / df_train.shape[0]
            if current_accuracy >= max_accuracy:
                best_threshold = n_seconds
                max_accuracy = current_accuracy
            print(f"For threshold = {n_seconds} accuracy = {current_accuracy:.3f}")
        print(f"Best threshold is {best_threshold} with accuracy: {max_accuracy:.3f}")
        with open(OUT_FILE_PATH, 'wb') as file:
            file.write(pickle.dumps(best_threshold))

    def predict_model(self, x):
        if not self.treshold:
            return None
        predictions = int(x[32] >= self.treshold)
        return predictions


if __name__ == '__main__':
    model = NaiveModel()
    model.train_model()
