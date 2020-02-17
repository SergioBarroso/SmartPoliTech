"""
Acción ejecutada al recibir un intent
"""
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import json

#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#

import neo4j_query

NEO4J_ATTRIBUTES = ["espacio", "sensor",
                    "orientacion", "edificio", "lugares", "nombre"]
INFLUXDB_ATTRIBUTES = ['hora_inicio', 'intervalo_anual', 'medida_limite',
                       'agrupacion_temporal', 'fecha_inicio', 'medida', 
                       'parte_dia', 'operacion_temporal', 'operacion', 
                       'fecha_fin', 'hora_fin', 'intervalo_temporal']
OCUPACION = ["ocupacion"]


class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        nlu = tracker.latest_message

        entities = list(
            map(lambda x: (x["value"], x["entity"]), nlu["entities"]))
        intent = (nlu["intent"]["name"], nlu["intent"]["confidence"])
        text = nlu["text"]

        if len(entities) == 0:
            dispatcher.utter_message(text="No se ha entendido la pregunta")
            return []

        entity_value, entity_name = zip(*entities)

        neo4j_entities = [(i, x)
                          for (i, x) in enumerate(entity_name) if x in NEO4J_ATTRIBUTES]
        influx_db_entities = [(i, x) for (i, x) in enumerate(
            entity_name) if x in INFLUXDB_ATTRIBUTES]
        ocupacion_entities = [(i, x)
                              for (i, x) in enumerate(entity_name) if x in OCUPACION]

        query_neo = neo4j_query.create_query(neo4j_entities, entity_value)

        print("---------------\nPregunta: ")
        print(text)
        print("---------------")
        print("---------------\nEntidades: ")
        print(entities)
        print("---------------")
        print("---------------\nIntent: ")
        print(intent)
        print("---------------")

        print("neo4j", neo4j_entities)
        print("influxdb", influx_db_entities)
        print("ocupacion", ocupacion_entities)

        print("---------------\nQuery Neo: ")
        print(query_neo)
        print("---------------")

        # tracker.latest_message tiene la respuesta del nlu del úlyimo mensaje
        #dispatcher.utter_message(
        #text=json.dumps({"resp": tracker.latest_message, "entities" : entities,
        #                 "intent" : intent }))
        dispatcher.utter_message(text=json.dumps(tracker.latest_message))

        return []
