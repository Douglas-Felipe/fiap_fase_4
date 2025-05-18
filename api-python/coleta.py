from flask import Flask, request, jsonify
import pymysql


# logica para listar os dados coletados pelos sensoores em locais de plantação na base de dados
def lista_coletas_local(db_config, local):

    try:
        # se conecta com a base de dadops
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT c.ts_coleta as data_coleta, c.cd_sensor as codigo_sensor, s.nm_sensor as nome_sensor, s.cd_local as codigo_local, l.nm_local as nome_local, c.vl_coleta as valor_coletado, c.tp_indicador as tipo_indicador  FROM t_coleta c inner join t_sensor s on c.cd_sensor = s.cd_sensor inner join t_local l on s.cd_local = l.cd_local where s.cd_local = %s order by c.ts_coleta desc"
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



# logica para registrar a coleta de um sensor em um local de plantação na base de dados
def registra_coleta(db_config):
    dados = request.get_json()
    sensor = dados.get('codigo_sensor')
    valor = dados.get('valor_coletado')
    tipo_indicador = dados.get('tipo_indicador')


    # verificar se os campos obrigatórios foram informados
    if not sensor or valor is None or not tipo_indicador:
        return jsonify({"erro": "Campos obrigatórios: codigo_sensor, valor_coletado, tipo_indicador"}), 400

    try:
        # se conecta com a base de dados
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO t_coleta (ts_coleta, cd_sensor, vl_coleta, tp_indicador) VALUES (NOW(), %s, %s, %s)"
        # executa a consulta SQL
        cursor.execute(sql, (sensor, valor, tipo_indicador))
        conn.commit()
        return jsonify({"mensagem": "Coleta  registrada com sucesso!"}), 201
    except Exception as e:
        # qualquer erro que ocorrer na execução do código, ele será tratado aqui e retornado como Json para o usuario
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn is not None:
          conn.close()