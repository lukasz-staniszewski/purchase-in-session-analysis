import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def create_model():
    return RandomForestClassifier()


def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)


def main():
    train_df = pd.read_json(path_or_buf='../../../data/processed/train_set.jsonl')
    model = create_model()
    train_model(model, train_df.drop(columns=['index', 'purchased']).values, train_df['purchased'])
    pickle.dump(model, open("../../../models/random_forest/random_forest.sav", "wb"))


if __name__ == '__main__':
    main()
