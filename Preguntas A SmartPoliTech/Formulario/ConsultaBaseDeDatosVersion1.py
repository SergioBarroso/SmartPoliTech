from __future__ import absolute_import, division, print_function, unicode_literals
from influxdb import InfluxDBClient
import json
from py2neo import Graph, Node
from py2neo import Node, Relationship
from py2neo import Database
import sys, time
from neo4j import GraphDatabase

#5-¿Qué temperatura media diaria de 10:30 a 12:30 hay en salas no ocupadas? respondida
# ¿Que sala ocupada tiene una concentración de CO2 por encima de 800ppm?
# ¿Donde está la room de no se quien



"""*************************Conexiones con INfluxDB y Neo4j*************************************************"""

client = InfluxDBClient(host='10.253.247.18', port=8086, username='r0b0l4b', password='alwayssmarter4')
client.switch_database('sensors')
graph=Graph("bolt://158.49.112.122:7687", auth=("Smart", "Politech"))


"""*********************************************************************************************************"""
"""*********************************************Querys a Neo4J**********************************************"""




#Hacerlo dependiente del tipo de sensor (type)


def Query_Salas(Tipo_Sensor, graph, ocupada):#Cuando nos piden analiazar las salas en función de una medida, añadiria booleano si está pidiendo salas ocupadas o si eso da igual
    Sensores_Analizar = []
    Salas_Analizar=[]
    if ocupada:
        results = graph.run("MATCH (a:Room),(b:Device) WHERE b.type = $type and a.estado= $estado and (a)-[:HAS]->(b) "
                            "RETURN a as Sala, b as Nombre_Sensor",
                            type=Tipo_Sensor, estado="ocupada").data()  # .data() para convertir el resultado obtenido en lista
    else:
        results = graph.run("MATCH (a:Room),(b:Device) WHERE b.type = $type and (a)-[:HAS]->(b)"
                            "RETURN a as Sala, b as Nombre_Sensor",
                            type=Tipo_Sensor).data()  # .data() para convertir el resultado obtenido en lista
    for r in results:
        sensor = r["Nombre_Sensor"]
        salas= r["Sala"]
        Sensores_Analizar.append(sensor["id"])
        Salas_Analizar.append(salas["id"])
    return Sensores_Analizar, Salas_Analizar





"""**************************************************************************************************************"""

"""Querys a Influx"""
"""
   fromDate="2020-01-01T10:00:00Z" #puede ser cualquier fecha que nos llegue, o igual hay que construirla a partir de la pregunta
   medida="temp"#La medida que se haya solicitado en la peticion
   operacion="mean"#operqacion que se haya pedido  en la peticion
   """

def Query_Media_Medida(client, Sensores, medida, operacion, fecha): # client: conexión a influx, Sensores: tablas a analizar en influx, medida: medida a analizar, operación a aplicar, fecha: fecha a partir de la cual analizar
    #results=[]#Esto hay que pensar como devolver los resultados, de momento
    resultados_sensor={}
    for s in Sensores:
        query = "Select mean(%s) from  (select mean(%s) from %s where time >= '%s' GROUP BY time(2h)) WHERE time > '%s' GROUP BY time(24h,10h) " % (operacion, medida, s, fecha, fecha)
        resultados_sensor.update({s : list(client.query(query))})
        # results.append(list(client.query(query)))
    return resultados_sensor

def Query_level(client, Sensores, medida, nivel, condicion ):
    resultados_sensor = {}
    if condicion=="encima":
        for s in Sensores:
            query = "select %s from %s where %s > %s and time > now()-1h " % ( medida, s, medida, nivel[0])
            resultados_sensor.update({s : list(client.query(query))})
    elif condicion=="debajo":
        for s in Sensores:
            query = "select %s from %s where %s < %s and time > now()-1h " % ( medida, s, medida, nivel[0])
            resultados_sensor.update({s : list(client.query(query))})
    elif condicion=="entre":
        for s in Sensores:
            query = "select %s from %s where %s > %s and %s < %s and time > now()-20m " % ( medida, s, medida, nivel[0], medida, nivel[1])
            resultados_sensor.update({s : list(client.query(query))})

    return resultados_sensor





"""******************Pruebas*************************"""
Sensores, Salas=Query_Salas("thr", graph, False)
print(Salas)
resultados=Query_Media_Medida(client, Sensores, "temp", "mean", "2020-01-01T10:00:00Z" )
resultados=Query_level(client, Sensores, "temp", [15, 20], "entre")
print(resultados)
"""*****************************************"""







"""

Con otra librería para neo
#url = "bolt://localhost:7687"
url = "bolt://158.49.112.122:7687"
driver = GraphDatabase.driver(url, auth=("Smart", "Politech"))



def print_BuildingName(tx, name):
    for record in tx.run("MATCH (a:Building) WHERE a.id = $id "
    "RETURN a", id=id):
        print(record["a.name"])

with driver.session() as session:
    session.read_transaction(print_BuildingName("UEXCC_INF"))

print("Peticion correcta")
"""