from sqlalchemy import create_engine
import pandas as pd
import os

DATABASE_URL = os.environ['DATABASE_URL']

if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')

engine = create_engine(DATABASE_URL)


def get_cities():
    query = 'SELECT * FROM public.cities'
    data = pd.read_sql(query, engine).set_index('id')
    return data


def save_trips(trips):
    result = trips.to_sql('raw_data_aguia_branca', engine, schema='public', if_exists='append', index=False)
    return trips


def get_last():
    query = 'SELECT MAX(gathered_at) FROM raw_data_aguia_branca'
    data = pd.read_sql(query, engine)
    return str(data['max'].values[0])


def number_of_data():
    query = 'SELECT count(id) FROM raw_data_aguia_branca'
    data = pd.read_sql(query, engine)
    return data


def get_all_data():
    query = 'SELECT servico as "Serviço", data_corrida as "Data",	origem as "Origem", destino as "Destino", classe as "Classe", saida as "Saida", chegada as "Chegada", assentos_livres as "Assentos livres", assentos_totais as "Assentos totais", preco as "Preço", gathered_at as "Coletado em" FROM raw_data_aguia_branca'
    data = pd.read_sql(query, engine)
    return data
