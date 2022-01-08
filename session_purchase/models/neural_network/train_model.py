import tensorflow as tf
import numpy as np
import pandas as pd


def create_model(in_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_dim=in_size),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation="sigmoid")

    ])
    return model


def train_model(model, X_train, y_train, num_epochs):
    model.fit(np.array(X_train, dtype=np.float64), np.array(y_train, dtype=np.float64), epochs=num_epochs)
    return model


def main():
    train_df = pd.read_json(path_or_buf='../../../data/processed/train_set.jsonl')
    model = create_model(train_df.shape[1] - 2)
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(),
                  metrics=['accuracy'])
    model = train_model(model, train_df.drop(columns=['session_id', 'purchased']), train_df['purchased'], num_epochs=200)
    model.save("../../../models/nn")


if __name__ == '__main__':
    main()
