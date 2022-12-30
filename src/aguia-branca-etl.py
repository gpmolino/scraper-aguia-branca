from prefect import task, Flow
from datetime import timedelta, datetime
from prefect.schedules import IntervalSchedule
import requests
from bs4 import BeautifulSoup
import pandas as pd
import database as db


@task
def extract():
    # Setup variables
    data = []
    labels_list = ['idOrigem', 'origem', 'idDestino', 'destino', 'data', 'dataCorrida', 'servico', 'grupo', 'saida',
                   'chegada', 'classe', 'empresa', 'assentos-livres', 'assentos-totais', 'preco', 'hasConexao',
                   'direction']
    cities = db.get_cities()

    for origin in cities['alias']:
        for destination in cities['alias']:
            if origin != destination:
                # Get HTML page
                try:
                    response = requests.get(f'https://www.aguiabranca.com.br/onibus/{origin}/{destination}')
                    if response.status_code != 200:
                        print(
                            f'Erro na requisição para https://www.aguiabranca.com.br/onibus/{origin}/{destination}')
                except Exception as err:
                    print(f'Unexpected {err=}, {type(err)=}')
                    # Break

                # Create BeautifulSoup object from html file
                soup = BeautifulSoup(response.text, 'html.parser')

                # Check if there is at least one trip
                if not bool(soup.find_all(id=0)):
                    print(f'Nenhuma viagem foi encontrada entre {origin} - {destination}')
                else:
                    # Scraping process
                    index = 0
                    while bool(soup.find_all(id=index)):
                        trip_data = {}
                        for label in labels_list:
                            trip_data[label] = soup.find('div', class_=f'offeringlist-info-{index} {label}').text
                        data.append(trip_data)
                        index += 1
                    print(f'{index + 1} viagem(s) encontrada(s) entre {origin} - {destination}')
    data = pd.DataFrame.from_dict(data)
    data['gathered_at'] = datetime.utcnow()
    return data

@task
def transform(data):
    # Fix date formats
    data['data'] = pd.to_datetime(data['data'])
    data['dataCorrida'] = pd.to_datetime(data['dataCorrida'])
    data['saida'] = pd.to_datetime(data['saida'])
    data['chegada'] = pd.to_datetime(data['chegada'])
    data['gathered_at'] = pd.to_datetime(data['gathered_at'])

    # Rename columns to match database table
    data.rename(inplace=True, columns={'idOrigem': 'id_origem', 'idDestino': 'id_destino', 'dataCorrida': 'data_corrida', 'assentos-livres': "assentos_livres", 'assentos-totais': 'assentos_totais', 'hasConexao': 'has_conexao'})
    return data


@task()
def load(data):
    db.save_trips(data)


schedule = IntervalSchedule(
    interval=timedelta(minutes=60))


with Flow("aguia-branca-flow", schedule=schedule) as flow:
    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)

flow.run()
