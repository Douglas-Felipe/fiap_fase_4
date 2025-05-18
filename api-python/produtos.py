from flask import Flask, request, jsonify
import pymysql


# logica para listar os Produtos que podem ser aplicados em locais de plantação na base de dados
def lista_produtos(db_config):

    try:
        # se conecta com a base de dadops
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT cd_produto as codigo, ds_produto as nome FROM t_produto order by ds_produto"
        # executa a consulta SQL
        cursor.execute(sql)
        # salva o resultado da consulta em uma variável
        produtos = cursor.fetchall()
        return jsonify(produtos), 200
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
          conn.close()

# logica para excluir um produto  na base de dados, este local nao pode ter sido aplicado em um local de plantacao
def excluir_produto(db_config, codigo):
    try:
        # se conecta com a base de dados
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        sql = "DELETE FROM t_produto WHERE cd_produto = %s"
        # executa a consulta SQL
        cursor.execute(sql, (codigo,))
        conn.commit()
        return jsonify({"mensagem": "Produto excluido com sucesso!"}), 200
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
          conn.close()


# logica para criar no novo produto na base de dados
def criar_produto(db_config):
    dados = request.get_json()
    nome = dados.get('nome')

    # verificar se os campos obrigatórios foram informados
    if not nome :
        return jsonify({"erro": "Campos obrigatórios:  nome"}), 400

    try:
        # se conecta com a base de dados
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO t_produto (ds_produto) VALUES (%s)"
        # executa a consulta SQL
        cursor.execute(sql, (nome))
        conn.commit()
        return jsonify({"mensagem": "Produto incluido com sucesso!"}), 201
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
          conn.close()