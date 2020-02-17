#!/bin/bash


if [ "$1" = "--interactive" ];
then
gnome-terminal --tab --title="rasa interactive server" -- bash -c "rasa interactive"
else 
gnome-terminal --tab --title="rasa server" -- bash -c "rasa run"
fi
sleep 1
gnome-terminal --tab --title="rasa actions server" -- bash -c "rasa run actions"
sleep 1
gnome-terminal --tab --title="rasa duckling server" -- bash -c "sudo docker run -p 8000:8000 rasa/duckling"
#
# url en la que escucha el servidor nlu: http://localhost:5005/webhooks/rest/webhook
# mensajes:
# {
#	"sender": "nombre",
#	"message": "Hola"
# }
#
# Duckling: curl -XPOST http://0.0.0.0:8000/parse --data 'locale=es_ES&text=mensaje'