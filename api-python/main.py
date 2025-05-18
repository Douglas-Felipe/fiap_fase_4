from flask import Flask, request, jsonify
import locais
import sensores
import produtos
import aplicacao
import coleta
import pymysql
from dotenv import load_dotenv
import os
app = Flask(__name__)


# Carrega as variáveis de ambiente do arquivo .env
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

# Rota GET para listar os locais de plantação
@app.route('/local', methods=['GET'])
def bff_lista_locais():
    return locais.lista_locais(db_config)

# Rota POST para criar um local de plantação
@app.route('/local', methods=['POST'])
def bff_cria_novo_local():
    return locais.criar_local(db_config)

# Rota DELETE para excluir um local de plantação
@app.route('/local/<int:codigo>', methods=['DELETE'])
def bff_exclui_local(codigo):
    return locais.excluir_local(db_config,codigo)



# Rota GET para listar os sensores existentes em locais de plantação
@app.route('/sensor', methods=['GET'])
def bff_lista_sensores():
    return sensores.lista_sensor(db_config)

# Rota POST para registrar um novo em um local de plantação
@app.route('/sensor', methods=['POST'])
def bff_cria_novo_sensor():
    return sensores.criar_sensor(db_config)

# Rota DELETE para excluir um sensor de um local de plantação
@app.route('/sensor/<int:codigo>', methods=['DELETE'])
def bff_exclui_sensor(codigo):
    return sensores.excluir_sensor(db_config,codigo)



# Rota GET para listar os produtos que podem ser aplicados em locais de plantação
@app.route('/produto', methods=['GET'])
def bff_lista_produtos():
    return produtos.lista_produtos(db_config)

# Rota POST para registrar um novo produto
@app.route('/produto', methods=['POST'])
def bff_cria_novo_produto():
    return produtos.criar_produto(db_config)

# Rota DELETE para excluir um produto
@app.route('/produto/<int:codigo>', methods=['DELETE'])
def bff_exclui_produto(codigo):
    return produtos.excluir_produto(db_config,codigo)




# Rota GET para listar as aplicacoes de produtos aplicados em um local especifico de plantação
@app.route('/aplicacao/<int:codigo_local>', methods=['GET'])
def bff_lista_aplicacoes(codigo_local):
    return aplicacao.lista_aplicacoes(db_config,codigo_local)

# Rota POST para registrar um novo produto
@app.route('/aplicacao', methods=['POST'])
def bff_registra_aplicacao():
    return aplicacao.registra_aplicacao(db_config)



# Rota GET para listar as coeltas realziadas em um local especifico de plantação
@app.route('/coleta/<int:codigo_local>', methods=['GET'])
def bff_lista_coletas(codigo_local):
    return coleta.lista_coletas_local(db_config,codigo_local)

# Rota POST para registrar uma nova coleta
@app.route('/coleta', methods=['POST'])
def bff_registra_coleta():
    return coleta.registra_coleta(db_config)




if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)
