import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("👩🏽‍🏫 DocentES 👨🏻‍🏫")
st.write(
    "Bem-vindo à DocentES, a plataforma sobre os Docentes do Espírito Santo!"
)

# Carregar dataset
@st.cache_data
def carregar_dados(name):
    return pd.read_csv(name, sep=";")

df_etapa = carregar_dados("docentes_etapas.csv")

# Mostrar dados
st.subheader("🔍 Visualização da Tabela de Dados")
st.dataframe(df_etapa)