from flask import Flask, request, jsonify
import pymysql


# logica para listar os sensores instalados em locais de plantação na base de dados
def lista_sensor(db_config):

    try:
        # se conecta com a base de dadops
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT s.cd_sensor as codigo_sensor, s.nm_sensor as nome_sensor, s.cd_local as codigo_local, l.nm_local nome_local FROM t_sensor s inner join t_local l on s.cd_local = l.cd_local order by s.nm_sensor"
        # executa a consulta SQL
        cursor.execute(sql)
        # salva o resultado da consulta em uma variável
        sensores = cursor.fetchall()
        return jsonify(sensores), 200
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
          conn.close()

# logica para excluir um sensor instalado em um local na base de dados, este sensor nao pode ter sido utilizado em uma coleta
def excluir_sensor(db_config, codigo):
    try:
        # se conecta com a base de dados
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        sql = "DELETE FROM t_sensor WHERE cd_sensor = %s"
        # executa a consulta SQL
        cursor.execute(sql, (codigo,))
        conn.commit()
        return jsonify({"mensagem": "Sensor excluido com sucesso!"}), 200
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
          conn.close()


# logica para  criar no novo sensor em um local de plantacao na base de dados
def criar_sensor(db_config):
    dados = request.get_json()
    codigo_local =  dados.get('codigo_local')
    nome = dados.get('nome')

    # verificar se o nome do local foi informado 
    if not nome or not codigo_local:
        return jsonify({"erro": "Campos obrigatórios: codigo_local, nome"}), 400

    try:
        # se conecta com a base de dados
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO t_sensor (cd_local, nm_sensor) VALUES (%s, %s)"
        # executa a consulta SQL
        cursor.execute(sql, (codigo_local, nome))
        conn.commit()
        return jsonify({"mensagem": "Sensor incluido com sucesso!"}), 201
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
          conn.close()