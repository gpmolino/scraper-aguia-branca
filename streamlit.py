import streamlit as st
import services

st.sidebar.title('Aguia Branca Scrapper')
origin = st.sidebar.selectbox('Origem', ['linhares-es', 'vitoria-es', 'colatina-es', 'vicosa-mg'])
destination = st.sidebar.selectbox('Destino', ['linhares-es', 'vitoria-es', 'colatina-es', 'vicosa-mg'])

st.table(services.aguia_branca_trips(origin, destination))
