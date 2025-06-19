from flask import Flask, request, jsonify
import pymysql


# logica para listar os locais de plantação na base de dados
def lista_locais(db_config):
    conn = None
    try:
        # se conecta com a base de dadops
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT cd_local as codigo, nm_local as nome FROM t_local order by cd_local"
        # executa a consulta SQL
        cursor.execute(sql)
        # salva o resultado da consulta em uma variável
        locais = cursor.fetchall()
        return jsonify(locais), 200
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn:
            conn.close()

# logica para excluir um local na base de dados, este local nao pode ter sido utilizado em uma coleta
def excluir_local(db_config, codigo):
    conn = None
    try:
        # se conecta com a base de dados
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        sql = "DELETE FROM t_local WHERE cd_local = %s"
        # executa a consulta SQL
        cursor.execute(sql, (codigo,))
        conn.commit()
        return jsonify({"mensagem": "Local excluido com sucesso!"}), 200
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


# logica para  criar no novo local na base de dados
def criar_local(db_config):
    dados = request.get_json()
    nome = dados.get('nome')
    conn = None

    # verificar se o nome do local foi informado 
    if not nome :
        return jsonify({"erro": "Campos obrigatórios:  nome"}), 400

    try:
        # se conecta com a base de dados
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO t_local (nm_local) VALUES (%s)"
        # executa a consulta SQL
        cursor.execute(sql, (nome))
        conn.commit()
        return jsonify({"mensagem": "Local incluido com sucesso!"}), 201
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()