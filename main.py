import requests
import sys
import logging
from bs4 import BeautifulSoup

# Get from user origin and destination
print('--- AGUIA BRANCA WEB SCRAPER ---')
city_origin = input('Origem: ')
city_destination = input("Destino : ")

# Setup variables
trip_list = []
labels_list = ['idOrigem', 'origem', 'idDestino', 'destino', 'data', 'dataCorrida', 'servico', 'grupo', 'saida',
               'chegada', 'classe', 'empresa', 'assentos-livres', 'assentos-totais', 'preco', 'hasConexao', 'direction']

# Get HTML page
try:
    response = requests.get(f'https://www.aguiabranca.com.br/onibus/{city_origin}/{city_destination}')
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
    logging.info(f'Nenhuma viagem foi encontrada entre {city_origin} - {city_destination}')
else:
    # Scraping process
    index = 0
    while bool(soup.find_all(id=index)):
        trip_data = {}
        for label in labels_list:
            trip_data[label] = soup.find('div', class_=f'offeringlist-info-{index} {label}').text
        trip_list.append(trip_data)
        index += 1

# Display results formatted
if len(trip_list) == 0:
    print('Nenhuma viagem foi encontrada entre essas cidades.')
else:
    for trip in trip_list:
        print('{0} -> {1} - {2} - R${3}'.format(trip['saida'], trip['chegada'], trip['classe'], trip['preco']))
        print('     {2} - R${3}'.format(trip['saida'], trip['chegada'], trip['classe'], trip['preco']))
