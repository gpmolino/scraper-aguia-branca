import streamlit as st
import database as db

st.set_page_config(
    page_title="Bus Scrapper",
    layout="wide",
)

cities = db.get_cities()
all_data = db.get_all_data()

st.title('Bus Scrapper')

st.metric(label='Número de registros', value=db.number_of_data().values)
st.metric(label='Data/hora da última coleta', value=db.get_last())

st.dataframe(all_data)

