import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def create_model():
    return RandomForestRegressor()


def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)


def main():
    train_df = pd.read_json(path_or_buf='../../../data/processed/train_set.jsonl')
    model = create_model()
    train_model(model, train_df.drop(columns=['session_id', 'purchased']).values, train_df['purchased'].values)
    pickle.dump(model, open("../../../models/random_forest/random_forest.sav", "wb"))


if __name__ == '__main__':
    main()
