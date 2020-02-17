"""
Crear consultas para neo4j
"""
TEMPLATE_NEO = "MATCH {} {} {} {} {} {} {} RETURN {}"

def create_query(neo4j_entities, entity_value):
    """
    Crear consultas para neo4j
    """

    def get_value(index):
        return SINONIMOS_NEO4J[entity_value[index]] if SINONIMOS_NEO4J.get(entity_value[index])\
                                                    else entity_value[index]

    get_query_part = {
        "espacio": lambda x: "(n:Room {{ type: '{}' }})".format(get_value(x)),
        "sensor": lambda x: ("(d:Device)", f" '{get_value(x)}' in d.type"),
        "orientacion": lambda x: " n.orientacion CONTAINS '{}'".format(get_value(x)),
        "edificio": lambda x: ("(b:Building)", " b.name CONTAINS '{}'".format(get_value(x))),
        "nombre": lambda x: ("(b:Building)", " b.name CONTAINS '{}'".format(get_value(x))),
        "lugares": lambda x: " n.name CONTAINS '{}'".format(get_value(x))
    }


    dic = {}
    for entity in neo4j_entities:
        key = entity[1]
        if entity[1] == "nombre":
            key = "edificio"
        dic[key] = get_query_part[entity[1]](entity[0])

    espacio = dic["espacio"] if dic.get("espacio") else ""
    sensor = dic["sensor"] if dic.get("sensor") else ("", "")
    orientacion = dic["orientacion"] if dic.get("orientacion") else ""
    edificio = dic["edificio"] if dic.get("edificio") else ("", "")
    lugares = dic["lugares"] if dic.get("lugares") else ""
    ret = []

    # crear relaciones que son opcionales en la consulta
    if espacio is not "" and sensor != ("", ""):
        sensor = (sensor[0]+"<-[:HAS]-", sensor[1])
    if espacio is not "" and edificio != ("", ""):
        espacio += "<-[:HAS]-(f:Floor)<-[:HAS]-"

    #Añadir información a la consulta que no se infica pero que es necesaria para poder recorrer las relaciones en Neo4j.
    
    # Si se pregunta por sensor y lugar pero no por espacio.
    if espacio is "" and sensor != ("", "") and lugares is not "":
        espaciocio = "(n:Room)"
        sensor = (sensor[0]+"<-[:HAS]-", sensor[1])
    # Si se pregunta por nombre u orientación pero no por espacio.
    if espacio is "" and (lugares is not "" or orientacion is not ""):
        espacio = "(n:Room)"
    # Si se pregunta por sensores en un edificio sin especificar un espacio.
    if espacio is "" and edificio != ("", "") and sensor != ("", ""):
        espacio = "(n:Room)<-[:HAS]-(f:Floor)<-[:HAS]-"
        sensor = (sensor[0]+"<-[:HAS]-", sensor[1])
    # Si hay 4
    # orientacion lugares edificio sensor
    #    X          X        X       X
    if orientacion is not "" and lugares is not "" and edificio != ("", "") and sensor != ("", ""):
        lugares = "AND " + lugares
        orientacion = "WHERE " + orientacion
        edificio = (edificio[0], "AND " + edificio[1])
        sensor = (sensor[0], "AND " + sensor[1])

    # Si hay 3
    # orientacion lugares edificio sensor
    #    X          X        X       -
    #    X          -        X       X
    #    -          X        X       X
    #    X          -        X       X
    if orientacion is not "" and lugares is not "" and edificio != ("", "") and sensor == ("", ""):
        lugares = "AND " + lugares
        orientacion = "WHERE " + orientacion
        edificio = (edificio[0], "AND " + edificio[1])
    if orientacion is not "" and lugares is not "" and edificio == ("", "") and sensor != ("", ""):
        lugares = "AND " + lugares
        orientacion = "WHERE " + orientacion
        sensor = (sensor[0], "AND " + sensor[1])
    if orientacion is "" and lugares is not "" and edificio != ("", "") and sensor != ("", ""):
        lugares = "WHERE " + lugares
        sensor = (sensor[0], "AND " + sensor[1])
        edificio = (edificio[0], "AND " + edificio[1])
    if orientacion is not "" and lugares is "" and edificio != ("", "") and sensor != ("", ""):
        orientacion = "WHERE " + orientacion
        sensor = (sensor[0], "AND " + sensor[1])
        edificio = (edificio[0], "AND " + edificio[1])

    # Si hay 2
    # orientacion lugares edificio sensor
    #    X          X        -       -
    #    X          -        X       -
    #    X          -        -       X
    #    -          X        X       -
    #    -          X        -       X
    #    -          -        X       X

    if orientacion is not "" and lugares is not "" and edificio == ("", "") and sensor == ("", ""):
        lugares = "AND " + lugares
        orientacion = "WHERE " + orientacion
    if orientacion is not "" and lugares is "" and edificio != ("", "") and sensor == ("", ""):
        edificio = (edificio[0], "AND " + edificio[1])
        orientacion = "WHERE " + orientacion
    if orientacion is not "" and lugares is "" and edificio == ("", "") and sensor != ("", ""):
        sensor = (sensor[0], "AND " + sensor[1])
        orientacion = "WHERE " + orientacion
    if orientacion is "" and lugares is not "" and edificio != ("", "") and sensor == ("", ""):
        edificio = (edificio[0], "AND " + edificio[1])
        lugares = "WHERE " + lugares
    if orientacion is "" and lugares is not "" and edificio == ("", "") and sensor != ("", ""):
        sensor = (sensor[0], "AND " + sensor[1])
        lugares = "WHERE " + lugares
    if orientacion is "" and lugares is "" and edificio != ("", "") and sensor != ("", ""):
        sensor = (sensor[0], "AND " + sensor[1])
        edificio = (edificio[0], "WHERE " + edificio[1])
    # Si  hay 1
    # orientacion lugares edificio sensor
    #    X          -        -       -
    #    -          X        -       -
    #    -          -        X       -
    #    -          -        -      X
    if orientacion is not "" and lugares is "" and edificio == ("", "") and sensor == ("", ""):
        orientacion = "WHERE " + orientacion
    if orientacion is "" and lugares is not "" and edificio == ("", "") and sensor == ("", ""):
        lugares = "WHERE " + lugares
    if orientacion is "" and lugares is "" and edificio != ("", "") and sensor == ("", ""):
        edificio = (edificio[0], "WHERE " + edificio[1])
    if orientacion is "" and lugares is "" and edificio == ("", "") and sensor != ("", ""):
        sensor = (sensor[0], "WHERE " + sensor[1])



    # Preparar los atributos de salida
    if espacio is not "":
        ret.append("n.name, n.id")
    if sensor != ("", ""):
        ret.append("d.id, d.type")
    if orientacion is not "":
        ret.append("n.orientacion")

    return TEMPLATE_NEO.format(sensor[0], espacio, edificio[0], orientacion,\
         lugares, edificio[1], sensor[1], ", ".join(ret))


SINONIMOS_NEO4J = {
    #sensores
    "humedad" : "hum",
    "Co2" : "co2",
    "temperatura" : "temp",
    "luz" : "ele",
    "conexiones": "ips",
    "agua": "agua",
    "camara": "cam",
    #orientacion
    "norte" : "Norte",
    "sur": "Sur",
    "este": "Este",
    "oeste": "Oeste",
    #espacios
    "comun": "Comun",
    "aseo": "Aseo",
    "sala": "Sala",
    "cuarto": "Cuarto",
    "despacho": "Despacho",
    "aula": "Aula",
    "laboratorio": "Laboratorio",
    #lugares
    "sol": "Smart Open Lab",
    "conserjeria": "conserjería",
    "secretaria": "secretaría",
    "cafeteria": "cafetería",
    #edificios
    "teleco": "Telecomunicaciones",
    "informática": "Informática",
    "edificación": "Arquitectura Técnica",
    "obras": "Obras",
    "central": "Servicios Comunes",
    "investigacion": "Investigación",
    "escuela politecnica": "Pabellón"
}
