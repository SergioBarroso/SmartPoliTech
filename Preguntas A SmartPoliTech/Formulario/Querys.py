from __future__ import absolute_import, division, print_function, unicode_literals
from influxdb import InfluxDBClient
import json
from py2neo import Graph, Node
from py2neo import Node, Relationship
from py2neo import Database
import sys, time
from neo4j import GraphDatabase
import csv
import datetime



class Consultas:

    def __init__(self,
                 influxhost='10.253.247.18',
                 port=8086,
                 username='r0b0l4b',
                 password='alwayssmarter4',
                 database='sensors',
                 neo="bolt://158.49.112.122:7687",
                 neouser="Smart",
                 neopass="Politech"
                 ):
        """Definición conexiones a Neo4j e InfluxDB
        influxhost= ip de la máquina donde está desplegado InfluxDB
        port= puerto de la máquina asignado a InfluxDB
        username= usuario máquina donde está desplegado InfluxDB
        password= contraseña máquijna donde está desplegado InfluxDB
        database= nombre de la base de datos desplegada en InfluxDB que se vaya a utilizar
        neo= dirección bolt para conexión a Neo4j
        neouser= usuario de Neo4j
        neopass= contraseña de Neo4j
        """
        self.__influxhost = influxhost
        self.__port = int(port)
        self._username = username
        self._password = password
        self._database = database
        self._neo=neo
        self._neouser=neouser

        client = InfluxDBClient(host=influxhost, port=port, username=username, password=password)
        client.switch_database(database)
        self.graph = Graph(neo, auth=(neouser, neopass))
        self.client=client


    def Query_Salas(self,
                    Sensores_Analizar=[],
                    Salas_Orientacion=[],
                    Salas_Analizar = [],
                    Tipo_Sensor="",
                    orientacion=False,
                    ocupada=False):  # Cuando nos piden analiazar las salas en función de una medida, añadiria booleano si está pidiendo salas ocupadas o si eso da igual
        """Definición de querys a Neo4j cuya respuesta sea una lista de salas que tengan una serie de atributos en
        concreo así como tengan un sensor de un tipo en concreto
        Sensores_Analizar= lista con los sensores que deben ser analizados en influx que actuará como parámetro de salida
        Salas_Analizar= Lista de las salas que cumplen las condiciones de búsqueda que actuará como parámetro de salida
        Tipo_Sensor= tipo de sensor que se quiera analizar, que se corresponderá con la medida a analizar: de momento debe ser hum, temp, co2,vbat,o window
        orientacion= puede ser Norte, Sur, este u oeste, servirá para filtrar las salas como respuesta dependiendo de su orientación
        ocupada= True o False, si queremos filtrar por habitaciones ocupadas o no"""
        """************************Variables**************************"""
        self.__Tipo_Sensor = Tipo_Sensor
        self.__ocupada = ocupada
        self.__orientacion = orientacion
        if orientacion==False:
            if ocupada:
                results = self.graph.run(
                    "MATCH (a:Room),(b:Device) WHERE $type in b.type and a.estado= $estado and (a)-[:HAS]->(b) "
                    "RETURN a as Sala, b as Nombre_Sensor, a.orientacion as Orientacion",
                    type=Tipo_Sensor, estado="ocupada").data()
            else:
                results = self.graph.run("MATCH (a:Room),(b:Device) WHERE $type in b.type and (a)-[:HAS]->(b)"
                                    "RETURN a as Sala, b as Nombre_Sensor, a.orientacion as Orientacion",
                                    type=Tipo_Sensor).data()  # .data() para convertir el resultado obtenido en lista
        else:
            if ocupada:
                results = self.graph.run(
                    "MATCH (a:Room),(b:Device) WHERE $type in b.type and a.estado= $estado and a.orientacion= $orientacion and (a)-[:HAS]->(b) "
                    "RETURN a as Sala, b as Nombre_Sensor, a.orientacion as Orientacion",
                    type=Tipo_Sensor, estado="ocupada", orientacion=orientacion).data()  # .data() para convertir el resultado obtenido en lista
            else:
                results = self.graph.run("MATCH (a:Room),(b:Device) WHERE $type in b.type and a.orientacion= $orientacion and (a)-[:HAS]->(b)"
                                    "RETURN a as Sala, b as Nombre_Sensor, a.orientacion as Orientacion",
                                    type=Tipo_Sensor, orientacion=orientacion).data()  # .data() para convertir el resultado obtenido en lista
        for r in results:
            sensor = r["Nombre_Sensor"]
            salas = r["Sala"]
            Sensores_Analizar.append(sensor["id"])
            Salas_Analizar.append(salas["name"])
            Salas_Orientacion.append(salas["orientacion"])
        return Sensores_Analizar, Salas_Analizar, Salas_Orientacion



    def Query_Orientacion(self,
                    Salas_Analizar=[],
                    Salas_Orientacion=[],
                    Tipo_Sala=False,
                    orientacion=""):  # Cuando nos piden analiazar las salas en función de una medida, añadiria booleano si está pidiendo salas ocupadas o si eso da igual
        """Definición de querys a Neo4j cuya respuesta sea una lista de salas que tengan una serie de atributos en
        concreo así como tengan un sensor de un tipo en concreto
        Sensores_Analizar= lista con los sensores que deben ser analizados en influx que actuará como parámetro de salida
        Salas_Analizar= Lista de las salas que cumplen las condiciones de búsqueda que actuará como parámetro de salida
        Tipo_Sensor= tipo de sensor que se quiera analizar, que se corresponderá con la medida a analizar: de momento debe ser hum, temp, co2,vbat,o window
        orientacion= puede ser Norte, Sur, este u oeste, servirá para filtrar las salas como respuesta dependiendo de su orientación
        ocupada= True o False, si queremos filtrar por habitaciones ocupadas o no"""
        """************************Variables**************************"""
        self.__Tipo_Sala = Tipo_Sala
        self.__orientacion = orientacion
        if Tipo_Sala==False:
            results = self.graph.run(
                "MATCH (a:Room) WHERE a.orientacion= $orientacion "
                "RETURN a as Sala, a.orientacion as Orientacion",
                 orientacion=orientacion).data()
        else:
            results = self.graph.run(
                "MATCH (a:Room) WHERE a.orientacion= $orientacion and a.type=$type  "
                "RETURN a as Sala, a.orientacion as Orientacion",
                orientacion=orientacion, type=Tipo_Sala).data()

        for r in results:
            salas = r["Sala"]
            Salas_Analizar.append(salas["name"])
            Salas_Orientacion.append(salas["orientacion"])
        return  Salas_Analizar, Salas_Orientacion




    """INTEGRADO EN EL FORMULARIO"""
    def query_localizacion(self,
                           Room="",
                           Persona=False,
                           Device=False,
                           Tipo_Sensor=False):#Determinar el lugar en el que se situa una persona, un tipo de sensor determinado o un sensor en específico AÑADIR PETICION PARA DETERMINAR DONDE ESTÁ UNA SALA
        """Definición querys a Neo4j con el objetivo de conocer la localización de un sensor, una persona una sala, una planta...."""

        """************************Variables**************************"""
        self.__Room = Room
        self.__Persona = Persona
        self.__Device = Device
        self.__Tipo_Sensor = Tipo_Sensor
        ListaSensores=[]

        if Persona!=False:
            results = self.graph.run(
                "MATCH (a:Room),(b:People),(c:Building), (d:Floor) WHERE b.name= $name and (a)-[:HAS]->(b) and (d)-[:HAS]->(a) and (c)-[:HAS]->(d) "
                "RETURN b.name as Profesor, b.id as Id_People, a.name as Sala, a.id as Id_Room, d.name as Planta, c.name as Edificio",
                name=Persona).data()
        elif Tipo_Sensor!=False:
            results = self.graph.run(
                "MATCH (a:Room),(b:Device),(c:Building), (d:Floor) WHERE $tipo in b.type and (a)-[:HAS]->(b) and (d)-[:HAS]->(a) and (c)-[:HAS]->(d) "
                "RETURN b.name as Nombre_Sensor, b.id as Id_Sensor, a.name as Sala, a.id as Id_Room, d.name as Planta, c.name as Edificio",
                tipo=Tipo_Sensor).data()
            for r in results:
                ListaSensores.append(r)
            results=ListaSensores
        elif Device != False:
            results = self.graph.run(
                "MATCH (a:Room),(b:Device),(c:Building), (d:Floor) WHERE b.id= $id and (a)-[:HAS]->(b) and (d)-[:HAS]->(a) and (c)-[:HAS]->(d) "
                "RETURN b.name as Tipo_Sensor, b.id as Id_Device, a.name as Sala, a.id as Id_Room, d.name as Planta, c.name as Edificio",
                id=Device).data()

        return results





    """INTEGRADO EN EL FORMULARIO"""
    def Query_Media_Medida(self,
                           Sensores_Analizar=[],
                           resultados_sensor={},
                           medida="temp",
                           operacion="mean",
                           fecha=False,
                           fecha_fin=False,
                           primera_hora=False,
                           segunda_hora=False):  # client: conexión a influx, Sensores: tablas a analizar en influx, medida: medida a analizar, operación a aplicar, fecha: fecha a partir de la cual analizar
        """************************Variables**************************"""
        self.__medida = medida #Definir la medida a analizar, de una lista de:
        self.__operacion = operacion #Definir la operación a realizar
        self._fecha = fecha#Definir la fecha a partir de la cual comenzar a analizar
        self._Sensores_Analizar = Sensores_Analizar #Respuesta de Query_Salas
        self._fecha_fin = fecha_fin
        self._primera_hora = primera_hora
        self._segunda_hora= segunda_hora
        if primera_hora!=False and segunda_hora != False:
            dif=segunda_hora-primera_hora
            diferencia = str(dif)+"h"
        if fecha ==False:
            if primera_hora==False:
                for s in Sensores_Analizar: #Media 365 dias
                    query = "Select mean(%s) from %s where time >= now()-365d "% (
                    medida, s)
                    resultados_sensor.update({s: list(self.client.query(query))})
            elif primera_hora and segunda_hora and fecha and fecha_fin:
                for s in Sensores_Analizar: #Media 365 dias
                    query = "Select mean(%s) from  (select mean(%s) from %s where time >= '%s' and time < '%s' GROUP BY time(%s)) WHERE time > '%s' and time < '%s' GROUP BY time(24h,10h) " % (
                operacion, medida, s, fecha, fecha_fin, diferencia, fecha, fecha_fin)
                    resultados_sensor.update({s: list(self.client.query(query))})
        elif fecha != False and fecha_fin != False and primera_hora==False and segunda_hora==False:
            for s in Sensores_Analizar: #Media 365 dias
                query = "Select mean(%s) from %s where time >= '%s' and time < '%s'" % (
             medida, s, fecha, fecha_fin)
                resultados_sensor.update({s: list(self.client.query(query))})
        elif fecha != False and fecha_fin != False and primera_hora != False and segunda_hora != False:
            for s in Sensores_Analizar:
                query = "Select mean(%s) from  (select mean(%s) from %s where time >= '%s' and time < '%s' GROUP BY time(%s)) WHERE time > '%s' and time < '%s' GROUP BY time(24h,10h) " % (
                    operacion, medida, s, fecha, fecha_fin, diferencia, fecha, fecha_fin)
                resultados_sensor.update({s: list(self.client.query(query))})
        return resultados_sensor





    """INTEGRADO EN EL FORMULARIO"""
    def Query_level(self,
                    resultados_sensor={},
                    Sensores_Analizar=[],
                    medida="temp",
                    nivel=[],
                    condicion=""):


        """************************Variables**************************"""
        self._Sensores_Analizar = Sensores_Analizar  # Respuesta de Query_Salas
        self.__medida = medida
        self.__nivel = nivel
        self.__condicion = condicion
        """********************************************************************"""

        """************************Querys***********************************"""
        if condicion == "Mayor":
            for s in Sensores_Analizar:
                query = "select last(%s) from %s where %s > %s and time > now()-1h " % (medida, s, medida, nivel[0])
                resultados_sensor.update({s: list(self.client.query(query))})
        elif condicion == "Menor":
            for s in Sensores_Analizar:
                query = "select last(%s) from %s where %s < %s and time > now()-1h " % (medida, s, medida, nivel[0])
                resultados_sensor.update({s: list(self.client.query(query))})
        elif condicion == "Entre":
            for s in Sensores_Analizar:
                query = "select last(%s) from %s where %s > %s and %s < %s and time > now()-1h " % (
                medida, s, medida, nivel[0], medida, nivel[1])
                resultados_sensor.update({s: list(self.client.query(query))})
        return resultados_sensor





    """INTEGRADO EN EL FORMULARIO"""
    def Query_Niv_Actual(self,
                         Sensores=[],
                         medida=""):
        self._Sensores= Sensores
        self._medida = medida
        resultado={}
        if medida=="agua":
            for s in Sensores:
                query = "Select first(*) from %s  where time > now()-20m" % (
                 s)
                resultado.update({s: list(self.client.query(query))})
        else:
            for s in Sensores:
                query = "Select first(%s) from %s  where time > now()-20m" % (
                medida, s)
                resultado.update({s: list(self.client.query(query))})

        return resultado





    """INTEGRADO EN EL FORMULARIO"""
    def Query_Estaciones(self,
                           Sensores_Analizar=[],
                           resultados_sensor={},
                           medida="temp",
                           operacion="mean",
                           estacion=False,
                           year=False,
                           nivel=[],
                           condicion="",
                           orientacion=False,
                           ocupada=False
                           ):  # client: conexión a influx, Sensores: tablas a analizar en influx, medida: medida a analizar, operación a aplicar, fecha: fecha a partir de la cual analizar
        """************************Variables**************************"""
        self.__medida = medida #Definir la medida a analizar, de una lista de:
        self.__operacion = operacion #Definir la operación a realizar
        self._estacion = estacion #Definir la fecha a partir de la cual comenzar a analizar
        self._Sensores_Analizar = Sensores_Analizar #Respuesta de Query_Salas
        self._year = year
        self.__nivel = nivel
        self.__condicion = condicion
        self.__orientacion = orientacion
        self.__ocupada = ocupada
        """********************************************************************"""
        if year!=False:
            if estacion=="Primavera":
                diainicio="20-03"
                diafinal="20-06"
                fecha=diainicio+"-"+year+"T00:00:00Z"
                fechafin=diafinal+"-"+year+"T00:00:00Z"
            elif estacion=="Invierno":
                diainicio="22-12"
                diafinal="19-03"
                yearfin=int(year)
                yearfin=yearfin+1
                yearfin=str(yearfin)
                fecha = diainicio +"-"+ year + "T00:00:00Z"
                fechafin = diafinal +"-"+ yearfin + "T00:00:00Z"
            elif estacion=="Otoño":
                diainicio="22-09"
                diafinal="21-12"
                fecha = diainicio +"-"+ year + "T00:00:00Z"
                fechafin = diafinal +"-"+ year + "T00:00:00Z"
            elif estacion=="Verano":
                diainicio="21-06"
                diafinal="21-09"
                fecha = diainicio +"-"+ year + "T00:00:00Z"
                fechafin = diafinal +"-"+ year + "T00:00:00Z"
            else:
                print("ERROR")
        else:
            print("ERROR")
        fecha = datetime.datetime.strptime(fecha, "%d-%m-%YT%H:%M:%SZ")
        fechafin = datetime.datetime.strptime(fechafin, "%d-%m-%YT%H:%M:%SZ")
        if condicion == "Mayor":
            for s in Sensores_Analizar:
                query = "select %s from(select mean(%s) from %s where time >= '%s' and  time <='%s') where %s > %s" % ('mean', medida, s,fecha, fechafin, 'mean', nivel[0])
                resultados_sensor.update({s: list(self.client.query(query))})
        elif condicion == "Menor":
            for s in Sensores_Analizar:
                query = "select %s from(select mean(%s) from %s where time >= '%s' and  time <='%s') where %s < %s" % ('mean', medida, s,fecha, fechafin, 'mean', nivel[0])
                resultados_sensor.update({s: list(self.client.query(query))})
        elif condicion == "Entre":
            for s in Sensores_Analizar:
                query = "select %s from(select mean(%s) from %s where time >= '%s' and  time <='%s') where %s >= %s and %s < %s" % ('mean', medida, s,fecha, fechafin, 'mean', nivel[0], 'mean', nivel[1])
                resultados_sensor.update({s: list(self.client.query(query))})
        else:
            for s in Sensores_Analizar:  # Media 365 dias
                query = "Select mean(%s) from %s where time >= '%s' and  time <='%s' " % (
                    medida, s, fecha, fechafin)
                resultados_sensor.update({s: list(self.client.query(query))})

        return resultados_sensor

"""
x=Consultas()
Sensores, Salas, Orienta=x.Query_Salas(Tipo_Sensor="vbat", ocupada=False)
#resultado=x.Query_Estaciones(Sensores_Analizar=Sensores, estacion="Verano", year="2019", nivel=[23],condicion="Mayor")
resultado=x.Query_Niv_Actual(Sensores=Sensores, medida="vbat")
print(resultado)
"""