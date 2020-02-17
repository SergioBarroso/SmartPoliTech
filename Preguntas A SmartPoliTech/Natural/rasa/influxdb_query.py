"""
Generar consultas para influx_db utilizando el lenguaje flux.
"""


TEMPLATE_NEO = "select {} from {} {} "

def create_query(sensores, influxdb_entities, entity_value, intent):
   
    def get_value(index):
        return  entity_value[index]


    get_query_part = {
        #mean, sum, etc
        "operacion_temporal": lambda x: get_temp_operation(x),
        # <= >=, el mayor, el menor. 
        "operacion": lambda x: get_operation(x),

        #día, mes, año, ahora range(start, end)
        "intervalo_temporal": lambda x: get_intervalo_temporal(x),
        #primavera, verano, otoño, invierno range(start, end)
        "intervalo_anual": lambda x: get_intervalo_anual(x),

        #fecha_inicio, fecha_fin range(start, end)
        "fecha_inicio": lambda x: "start: {}",
        "fecha_fin": lambda x: "stop: {}",

        #hora_inicia, hora_final hourSelection()
        "hora_inicio": lambda x: " start: {}",
        "hora_fin": lambda x: " stop: {}",#get_hora_fin,

        #semanal, diario, mensual, anual (group by)
        "agrupacion_temporal": lambda x: "  |> window(every: {}) ", #get_agrupacion_temporal,

        # filter
        "medida": lambda x:  "" , #get_medida
        "medida_limite": lambda x: "", #get_limite

        #hourSelection
        "parte_dia" : lambda x: "|> hourSelection(start: {}, stop: {})", #parte_dia(noche, tarde, mañana, etc.) 

        #otro
        "time" : lambda x: ""
    }

    dic = {}
    for entity in influxdb_entities:
        key = entity[1]
        if dic.get(key) is not None:
            dic[key].append(influxdb_entities[entity[1]](entity[0]))
        else:
            dic[key] = [influxdb_entities[entity[1]](entity[0])]

    
    operacion_temporal = dic["operacion_temporal"] if dic.get("operacion_temporal") else ""

    intervalo = dic["intervalo"] if dic.get("intervalo") else ""

    hora_inicio = dic["hora_inicio"] if dic.get("hora_inicio") else ""
    hora_fin = dic["hora_fin"] if dic.get("hora_fin") else ""

    operacion = dic["operacion"] if dic.get("operacion") else ""
    medida = dic["medida"] if dic.get("medida") else ""
    medida_limite = dic["medida_limite"] if dic.get("medida_limite") else ""

    #Que hacer cuando aparecen atributos de tipo time
    if dic.get("time"):
        pass

    def get_temp_operation(x):
        if x == "medio":
            return "mean()"
        elif x == "total":
            return "sum()"
        elif x == "el mayor":
            return "sort(collumns: ['{}'], desc: false) |> first()"
        elif x == "el menor":
            return "sort(collumns: ['{}'], desc: true) |> first()"
        return ""

    def get_operation(x):
        if x == "<=":
            return " |> filter(fn: (r) => {} <= r.value)  "
        elif x == ">=":
            return " |> filter(fn: (r) => {} >= r.value)  "
        elif x == "desde":
            return " |> filter(fn: (r) => {} >= r.value)  "
        elif x == "hasta":
            return " |> filter(fn: (r) => {} >= r.value)  "
        return ""

    def get_intervalo_temporal(x):
        if x == "día":
            return " |> range(start: -1d)  "
        elif x == "mes":
            return "  |> range(start: -30d)   "
        elif x == "año":
            return "  |> range(start: -1y)  "
        elif x == "ahora":
            return "  |> range(start: -10m)   "
        return ""

    def get_intervalo_anual(x):
        # si no formateo aquí quitar la función.
        if x == "primavera":
            return " |> range(start: {}, stop: {})  "
        elif x == "verano":
            return " |> range(start: {}, stop: {})  "
        elif x == "otoño":
            return " |> range(start: {}, stop: {})  "
        elif x == "invierno":
            return " |> range(start: {}, stop: {})  "
        return ""
    # Hay que comprobar que no haya incomptabilidad entre sentencias. Ej: Solo debería haber un range.


SINONIMOS_INFLUX = {
    #operaciones
    "el mayor": "",
    "el menor": "",
    "antes" : "<",
    "despues": ">",
    #operaciones_temporales
    "medio" : "media",
    "el mayor": "mayor",
    "el menor": "menor",
    #intervalos
    "ultimo mes": "30d",
    "última semana": "7d",
    "día" : "1d",
    
}