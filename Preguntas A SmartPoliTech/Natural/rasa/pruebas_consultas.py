import re
                      
TEMPLATE_NEO = "MATCH {} {} {} {} {} RETURN {}"
#Primero espacio, segundo sensor y tercero lugar
getValue = lambda index: entity_value[index]

espacio = ""
sensor = ""
orientacion = ""
edificio = ""
lugares = ""
ret = []


a = [('sala', 'espacio'), ('norte', 'orientacion'), ('teleco', 'nombre'), ('humedad', 'sensor')]

entity_value, entity_name = zip(*a) 

neo4jAttributes = ["espacio", "sensor", "orientacion",  "edificio", "lugares", "nombre"]
influxDBAttributes = ["sensor", "hora_inicio", "intervalo", "operacion_temporal", "medida" ,"medida_limite", "operacion","hora_fin"]
ocupacion = ["ocupacion"]

neo4jEntities = [(i,x) for (i,x) in enumerate(entity_name) if x in neo4jAttributes]
influxDBEntities = [(i,x) for (i,x) in enumerate(entity_name) if x in influxDBAttributes]
ocupacionEntities = [(i,x) for (i,x) in enumerate(entity_name) if x in ocupacion]



getQueryPart = {
    "espacio" : lambda x: "(n:Room {{ type: '{}' }})".format(getValue(x)),
    "sensor" : lambda x: "(d:Device {{ type: '{}' }})".format(getValue(x)),
    "orientacion": lambda x: " n.orientacion CONTAINS '{}'".format(getValue(x)),
    "edificio": lambda x: "(b:Building) WHERE  b.name CONTAINS '{}'".format(getValue(x)),
    "nombre": lambda x: "(b:Building) WHERE  b.name CONTAINS '{}'".format(getValue(x)),
    "lugares": lambda x: " n.name CONTAINS '{}'".format(getValue(x))
}

dic = {}
for x in neo4jEntities:
    key = x[1]
    if x[1] == "nombre":
        key = "edificio"
    dic[key] = getQueryPart[x[1]](x[0])


#n = [getQueryPart[x[1]](x[0]) for x in neo4jEntities]

espacio = dic["espacio"] if dic.get("espacio") else ""
sensor =  dic["sensor"] if dic.get("sensor") else ""
orientacion =  dic["orientacion"] if dic.get("orientacion") else ""
edificio =  dic["edificio"] if dic.get("edificio") else ""
lugares =  dic["lugares"] if dic.get("lugares") else ""


if espacio is not "" and sensor is not "":
    sensor +="<-[:HAS]-"
if espacio is not "" and edificio is not "":
    espacio += "<-[:HAS]-(f:Floor)<-[:HAS]-"
if orientacion is not "" and  lugares is "" and edificio is "":
    orientacion = "WHERE " + orientacion
if orientacion is "" and lugares is not "" and edificio is "":
    lugares = "WHERE " + lugares
if orientacion is not "" and lugares is not "" and edificio is "":
    lugares = "AND " + lugares
    orientacion = "WHERE " + orientacion
if orientacion is not ""  and edificio is not "":
    orientacion = "AND " + orientacion
if lugares is not "" and edificio is  not"":
    lugares = "AND " + lugares

if espacio is not "":
    ret.append("n.name, n.id")
if sensor is not "":
    ret.append("d.id, d.type")
if orientacion is not "":
    ret.append("n.orientacion")

print(TEMPLATE_NEO.format(sensor, espacio, edificio, orientacion, lugares, ", ".join(ret) ))
print(neo4jEntities)
print(influxDBEntities)
