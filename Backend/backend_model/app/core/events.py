from fastapi import FastAPI
from core.config import POSTGRE, MODEL_IP, REDIS_PORT
from direct_redis import DirectRedis
from sqlalchemy import create_engine
import pandas as pd

redis_client = DirectRedis(host=MODEL_IP, port=REDIS_PORT)

def redis_use():
    if POSTGRE == 'False':
        # read csv file
        game_table = pd.read_csv('data/game.csv', encoding='cp949')
        cb_model_table = pd.read_csv('data/cb_model.csv')
        Ease_table = pd.read_csv('data/Ease.csv')
        cf_table = pd.read_csv('data/cf_model.csv')
        details_table = pd.read_csv('data/details.csv')
    else:
        # Create a sample DataFrame
        engine = create_engine(POSTGRE)
        game_table = pd.read_sql_table(table_name="game", con=engine)
        cb_model_table = pd.read_sql_table(table_name="cb_model", con=engine)
        Ease_table = pd.read_sql_table(table_name="Ease", con=engine)
        cf_table = pd.read_sql_table(table_name="cf_model", con=engine)
        details_table = pd.read_sql_table(table_name="details", con=engine)

    # Store DataFrame data in Redis with a key (e.g., 'df_cache')
    redis_client.set('game', game_table)
    redis_client.set('cb_model', cb_model_table)
    redis_client.set('Ease', Ease_table)
    redis_client.set('cf_model', cf_table)
    redis_client.set('details', details_table)
