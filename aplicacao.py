from flask import Flask, request, jsonify
import pymysql


# logica para listar os Produtos que foram aplicados em locais de plantação na base de dados
def lista_aplicacoes(db_config, local):

    try:
        # se conecta com a base de dadops
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT a.ts_aplicacao as data_aplicacao, a.cd_produto as codigo_produto, p.ds_produto as nome_produto, a.cd_local as codigo_local, l.nm_local as nome_local, a.qt_produto as quantidade  FROM t_aplicacao a inner join t_produto p on a.cd_produto = p.cd_produto inner join t_local l on a.cd_local = l.cd_local where a.cd_local = %s order by a.ts_aplicacao desc"
        # executa a consulta SQL
        cursor.execute(sql, (local))
        # salva o resultado da consulta em uma variável
        aplicacoes = cursor.fetchall()
        return jsonify(aplicacoes), 200
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
          conn.close()



# logica para registrar a aplicacao de um produto em um local de plantação na base de dados
def registra_aplicacao(db_config):
    dados = request.get_json()
    local = dados.get('codigo_local')
    produto = dados.get('codigo_produto')
    quantidade = dados.get('quantidade')

    # verificar se os campos obrigatórios foram informados 
    if not local or not produto or not quantidade:
        return jsonify({"erro": "Campos obrigatórios:  codigo_local, codigo_produto, quantidade"}), 400

    try:
        # se conecta com a base de dados
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO t_aplicacao (ts_aplicacao, cd_local, cd_produto, qt_produto) VALUES (NOW(), %s, %s, %s)"
        # executa a consulta SQL
        cursor.execute(sql, (local, produto, quantidade))
        conn.commit()
        return jsonify({"mensagem": "Aplicacao registrada com sucesso!"}), 201
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
          conn.close()