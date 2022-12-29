import streamlit as st
import services

st.title('Aguia Branca Scrapper')
origin = st.selectbox('Origem', ['linhares-es', 'vitoria-es', 'colatina-es', 'vicosa-mg'])
destination = st.selectbox('Destino', ['linhares-es', 'vitoria-es', 'colatina-es', 'vicosa-mg'])

st.table(services.aguia_branca_trips(origin, destination))
