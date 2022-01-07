# -*- coding: utf-8 -*-
from typing import Tuple, Any

import click
import logging
from pathlib import Path

import pandas as pd
from pandas import DataFrame


def one_hot_encoding(df: pd.DataFrame, column, delimiter=None):
    if delimiter:
        return df[column].str.get_dummies(delimiter)
    return df[column].str.get_dummies()


def apply_one_hot_encoding(df: pd.DataFrame, column, delimiter=None) -> Tuple[DataFrame, Any]:
    one_hot_column = one_hot_encoding(df, column, delimiter=delimiter)
    df.drop(columns=[column], inplace=True)
    return df.join(one_hot_column), one_hot_column


def add_sex_column(df: pd.DataFrame):
    df['sex'] = ['Female' if name.split(' ')[0][-1] == 'a' else 'Male' for name in df['name']]
    df_users, sex_one_hot = apply_one_hot_encoding(df, 'sex')
    return df_users, sex_one_hot


def aggregate_sessions(df, one_hot_aggregations):
    aggregation_functions = {
        'timestamp': lambda t: [(t.max() - t.min()).seconds, t.min(), t.max()],
        'user_id': 'first',
        'product_id': 'unique',
        'event_type': lambda e: 1 if len(e.unique()) > 1 else 0,
        'offered_discount': 'first',
        'price': lambda p: p.sum()
    }

    for one_hot, fun in one_hot_aggregations.items():
        for i in one_hot.columns:
            aggregation_functions[i] = fun

    main_df = df.groupby(df['session_id']).aggregate(aggregation_functions)
    main_df.rename(columns={'event_type': 'purchased'}, inplace=True)

    return main_df


def encode_dates(main_df):
    return pd.DataFrame({
        "month": main_df['session_start'].dt.month,
        "day": main_df['session_start'].dt.day,
        "hour": main_df['session_start'].dt.hour,
        "dayofweek": main_df['session_start'].dt.dayofweek,
    })


def dummy_sum(a, b):
    """Used exclusively to showcase relative imports in tests. See
       tests/test_make_dataset.py in the repo.
    """
    return a + b


# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    df_sessions = pd.read_json(path_or_buf='../../data/raw/sessions.jsonl', lines=True)
    df_products = pd.read_json(path_or_buf='../../data/raw/products.jsonl', lines=True)
    df_users = pd.read_json(path_or_buf='../../data/raw/users.jsonl', lines=True)
    df_products, categories_one_hot = apply_one_hot_encoding(df_products, 'category_path', delimiter=';')
    df_users, sex_one_hot = add_sex_column(df_users)
    df = df_sessions.merge(df_products, left_on='product_id', right_on='product_id')
    df = df.merge(df_users, left_on='user_id', right_on='user_id')
    aggregation_functions = {
        'timestamp': lambda t: [(t.max() - t.min()).seconds, t.min(), t.max()],
        'user_id': 'first',
        'product_id': 'unique',
        'event_type': lambda e: 1 if len(e.unique()) > 1 else 0,
        'offered_discount': 'first',
        'price': lambda p: p.sum()
    }

    for i in categories_one_hot.columns:
        aggregation_functions[i] = lambda n: n.sum()

    for name in sex_one_hot.columns:
        aggregation_functions[name] = 'first'

    main_df = df.groupby(df['session_id']).aggregate(aggregation_functions)
    main_df.rename(columns={'event_type': 'purchased'}, inplace=True)

    timestamp_dict = [{'session_length': x[0], 'session_start': x[1], 'session_end': x[2]} for x in
                      main_df['timestamp']]
    timestamp_df = pd.DataFrame(timestamp_dict)
    main_df = pd.concat([main_df, timestamp_df], axis=1, join="inner")
    main_df.drop(columns=['timestamp'], inplace=True)
    main_df.index.name = 'session_id'
    main_df['n_views'] = [len(x) for x in main_df['product_id'].values]
    main_df.reset_index(inplace=True)
    main_df.drop(columns=['session_id', 'user_id', 'product_id'], inplace=True)
    main_df = main_df.join(encode_dates(main_df))
    main_df.drop(columns=['session_start', 'session_end'], inplace=True)
    main_df.to_json(path_or_buf='../../data/processed/dataset.jsonl', orient="records")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    main()
