
import streamlit as st
import pandas as pd
import pymysql
import altair as alt
import os

from dotenv import load_dotenv

load_dotenv()

st.title("Monitoramento de Umidade e pH do Solo")
st.write("Visualização temporal dos dados coletados por sensores de uma plantação.")

# Conexão com o banco
@st.cache_data
def carregar_dados():
    db_config = {
        "host": os.getenv('DB_HOST'),
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASS'),
        "database": os.getenv('DB_NAME')
    }
    conn = pymysql.connect(**db_config)
    
    query = '''
    SELECT DATE(ts_coleta) as data, tp_indicador, vl_coleta
    FROM t_coleta
    WHERE cd_sensor IN (3, 4)
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = carregar_dados()

# Pivotar dados
df['data'] = pd.to_datetime(df['data'])
df_pivot = df.pivot_table(
    index='data',
    columns='tp_indicador',
    values='vl_coleta',
    aggfunc='mean'
).reset_index()

# Filtro de datas
min_date = pd.to_datetime(df_pivot['data']).min()
max_date = pd.to_datetime(df_pivot['data']).max()

date_range = st.date_input("Selecione o intervalo de datas:", [min_date, max_date])

if len(date_range) != 2:
    st.stop()

start_date, end_date = date_range

# Aplicar filtro
df_filtrado = df_pivot[
    (df_pivot['data'].dt.date >= start_date) &
    (df_pivot['data'].dt.date <= end_date)
]

# Gráfico de Umidade
st.subheader("Variação da Umidade")
chart_umidade = alt.Chart(df_filtrado).mark_line().encode(
    x='data:T',
    y='Umidade:Q',
    tooltip=['data:T', 'Umidade:Q']
).properties(width=700, height=300)
st.altair_chart(chart_umidade, use_container_width=True)

# Gráfico de pH
st.subheader("Variação do pH")
chart_ph = alt.Chart(df_filtrado).mark_line(color='orange').encode(
    x='data:T',
    y='pH:Q',
    tooltip=['data:T', 'pH:Q']
).properties(width=700, height=300)
st.altair_chart(chart_ph, use_container_width=True)
