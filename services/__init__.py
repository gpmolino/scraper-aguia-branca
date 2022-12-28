import requests
import sys
import logging
from bs4 import BeautifulSoup


def aguia_branca_trips(origin: str, destination: str):
    # Setup variables
    trip_list = []
    labels_list = ['idOrigem', 'origem', 'idDestino', 'destino', 'data', 'dataCorrida', 'servico', 'grupo', 'saida',
                   'chegada', 'classe', 'empresa', 'assentos-livres', 'assentos-totais', 'preco', 'hasConexao', 'direction']

    # Get HTML page
    try:
        response = requests.get(f'https://www.aguiabranca.com.br/onibus/{origin}/{destination}')
        if response.status_code != 200:
            logging.critical(f'Erro na requisição para https://www.aguiabranca.com.br/onibus/{city_origin}/{city_destination}')
    except Exception as err:
        logging.critical(f'Unexpected {err=}, {type(err)=}')
        # Break
        sys.exit()

    # Create BeautifulSoup object from html file
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if there is at least one trip
    if not bool(soup.find_all(id=0)):
        logging.info(f'Nenhuma viagem foi encontrada entre {origin} - {destination}')
    else:
        # Scraping process
        index = 0
        while bool(soup.find_all(id=index)):
            trip_data = {}
            for label in labels_list:
                trip_data[label] = soup.find('div', class_=f'offeringlist-info-{index} {label}').text
            trip_list.append(trip_data)
            index += 1
        logging.info(f'{index+1} viagem(s) encontrada(s) entre {origin} - {destination}')

    return trip_list
