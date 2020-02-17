from zato.server.service import Service
import requests
import json
import base64
class avisos(Service):

    def influxCall(self):
        return "aviso"

    def handle(self):
        self.response.payload = json.dumps(self.influxCall())