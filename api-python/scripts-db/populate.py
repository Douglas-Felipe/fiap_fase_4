import os
from dotenv import load_dotenv
import pymysql
import random
from datetime import datetime, timedelta

# Conexão com o banco
load_dotenv()

# Configuração do banco de dados
# ele precisa esta em execução, duvidas consulte o item 2.2. e 2.3 do READM do repositorio
# estas informações estão vindo do arquivo .env
db_config = {
    "host": os.getenv('DB_HOST'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASS'),
    "database": os.getenv('DB_NAME')
}
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# IDs fixos com base no seu banco
sensor_umidade = 4
sensor_ph = 3
local_id = 2  # Plantação Soja 02
produto_irrigacao = 2
produto_adubo = 1

# Início do ano simulado
data_inicio = datetime(2024, 1, 1)
dias = 365

coletas = []
aplicacoes = []

# Estado das variáveis
umidade = 75.0
ph = 6.5

for i in range(dias):
    ts = data_inicio + timedelta(days=i)
    mes = ts.month
    dia = ts.day

    # Estações
    if mes in [12, 1, 2]:  # Verão
        umidade -= random.uniform(1.5, 2.5)
        ph += random.uniform(-0.05, 0.02)
    elif mes in [3, 4, 5]:  # Outono
        umidade -= random.uniform(1.0, 1.8)
        ph -= random.uniform(0.01, 0.03)
    elif mes in [6, 7, 8]:  # Inverno
        umidade -= random.uniform(0.5, 1.2)
        ph += random.uniform(-0.02, 0.01)
    else:  # Primavera
        umidade -= random.uniform(1.0, 2.0)
        ph += random.uniform(-0.04, 0.04)

    # Simulação de chuva (aumenta a umidade aleatoriamente)
    if random.random() < 0.05:
        umidade += random.uniform(10, 25)

    # Limites razoáveis
    umidade = max(0, min(umidade, 100))
    ph = max(4.5, min(ph, 8.5))

    # Coletas do dia
    coletas.append((ts, sensor_umidade, round(umidade, 2), 'Umidade'))
    coletas.append((ts, sensor_ph, round(ph, 2), 'pH'))

    # Lógica de aplicação:
    # - Irrigação se umidade < 35
    # - Adubo se pH < 5.5 ou pH > 7.5
    irrigou = False
    aplicou_adubo = False

    if umidade < 35:
        aplicacoes.append((ts, produto_irrigacao, local_id, 10.0))
        umidade += random.uniform(15, 25)  # efeito da irrigação
        irrigou = True

    if ph < 5.5 or ph > 7.5:
        aplicacoes.append((ts, produto_adubo, local_id, 5.0))
        ph += random.uniform(-0.2, 0.2)  # efeito do adubo (instável)
        aplicou_adubo = True

# Inserção no banco
cursor.executemany("""
    INSERT INTO t_coleta (ts_coleta, cd_sensor, vl_coleta, tp_indicador)
    VALUES (%s, %s, %s, %s)
""", coletas)

cursor.executemany("""
    INSERT INTO t_aplicacao (ts_aplicacao, cd_produto, cd_local, qt_produto)
    VALUES (%s, %s, %s, %s)
""", aplicacoes)

conn.commit()
cursor.close()
conn.close()

print(f"{len(coletas)} coletas e {len(aplicacoes)} aplicações inseridas com sucesso.")
