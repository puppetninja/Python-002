import re
from collections import Counter

from sqlalchemy import create_engine
import pymysql
import pandas as pd
import numpy as np
import jieba
from snownlp import SnowNLP


DB_INFO = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'valkyrie',
    'charset': 'utf8'
}


def run():
    # Load raw data from DB
    phones_df, comments_df = load_raw_data(DB_INFO)

    # Raw data manipulation
    cleanse_phones_comments(comments_df)
    cal_phone_emo_trends(phones_df, comments_df)


def load_raw_data(db_info):
    host = db_info['host']
    user = db_info['user']
    password = db_info['password']
    db = db_info['db']
    engine = create_engine(
        f'mysql+pymysql://{user}:{password}@{host}/{db}'
    )

    phones_sql = "SELECT * FROM `phones`"
    phones_comments_sql = "SELECT * FROM `phone_comments`"
    phones_df = pd.read_sql(phones_sql, con=engine)
    phones_comments_df = pd.read_sql(phones_comments_sql, con=engine)

    return phones_df, phones_comments_df


def cleanse_phones_comments(comments_df):
    # 去重
    comments_df.drop_duplicates(subset=['comment_content'], inplace=True)

    # 去除空值
    comments_df['phone_name'].replace('', np.nan, inplace=True)
    comments_df['comment_content'].replace('', np.nan, inplace=True)
    comments_df.dropna(
        subset=['phone_name', 'comment_content', 'comment_date'],
        how='any', inplace=True)

    write_df_to_sql(comments_df, 'phone_comments_cleansed', DB_INFO)


def write_df_to_sql(df, table, db_info):
    host = db_info['host']
    user = db_info['user']
    password = db_info['password']
    db = db_info['db']
    engine = create_engine(
        f'mysql+pymysql://{user}:{password}@{host}/{db}'
    )

    df.to_sql(table, con=engine, if_exists='replace')


def cal_phone_emo_trends(phones_df, comments_df):
    phone_opinions = []
    phone_id = 1
    for _, p_row in phones_df.iterrows():
        phone_name = p_row['phone_name']
        phone_comments = comments_df[comments_df['phone_name'] == phone_name]
        comments_emo = [SnowNLP(r['comment_content']).sentiments
                        for _, r in phone_comments.iterrows()]
        neg_emos = [c for c in comments_emo if c < 0.5]
        neg_ratio = len(neg_emos) / len(comments_emo)

        phone_opinions.append({
            'id': phone_id,
            'phone_name': phone_name,
            'positive': format((1 - neg_ratio)*100, '.3f'),
            'negative': format(neg_ratio*100, '.3f')
        })
        phone_id += 1

    df = pd.DataFrame(phone_opinions)
    write_df_to_sql(df, 'phone_opinions', DB_INFO)


if __name__ == '__main__':
    run()
