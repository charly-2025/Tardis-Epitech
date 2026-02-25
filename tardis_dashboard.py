import streamlit as st
import pandas as pd
import plotly.express as px #interactive charts
import joblib
st.set_page_config (
    page_title = "Real-Time Data Dashboard Trains Delay",
    page_icon = "Active",
    layout = "wide",
)

TARGET = "Retard moyen de tous les trains à l'arrivée"

CAUSE_COLS = [
    "Prct retard pour causes externes",
    "Prct retard pour cause infrastructure",
    "Prct retard pour cause gestion trafic",
    "Prct retard pour cause matériel roulant",
    "Prct retard pour cause gestion en gare et réutilisation de matériel",
    "Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH, correspondances)",
]
CAUSE_LABELS = [
    "Causes externes",
    "Infrastructure",
    "Gestion trafic",
    "Matériel roulant",
    "Gestion en gare",
    "Voyageurs",
]

@st.cache_data #anything you CAN store in a database(python, dataframe, API call)
def load_data():
    return pd.read_csv("cleaned_dataset.csv")


@st.cache_resource #anything you CAN'T store in a database(ML models, database connections)
def load_model():
    return joblib.load("model.pkl")



st.title("Real-Time Data Dashboard Trains Delay")
number = st.slider("Causes externes", 0, 100)
def stocks_to_str(stocks):
    return ",".join(stocks)


if "Retard moyen de tous les trains à l'arrivée" not in st.session_state:
    st.session_state.tickers_input = st.query_params.get(
        "stocks", stocks_to_str("Cause","Infrastructure","Gestion trafic","Matériel roulant","Gestion en gare","Voyageurs")
    ).split(",")