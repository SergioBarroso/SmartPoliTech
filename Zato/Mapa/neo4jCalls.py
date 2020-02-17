from zato.server.service import Service
import requests
import json
import base64
class Neo4jCalls(Service):
    def query(self):
        url = "http://158.49.112.122:7474/db/data/transaction/commit"
        headers = { "Authorization": 'Basic ' + base64.b64encode('Smart:Politech'.encode('utf-8')).decode("utf-8"),
            "X-Stream": "true",
            "Accept": "application/json; charset=UTF-8",
            "Content-Type": "application/json"}
        data = { "statements": [{"statement": "match (n) return n","resultDataContents": ["row", "graph", "rest"]}]}
        response = requests.post(url, 
            data=json.dumps(data),
            headers=headers)
        return response.content

    def handle(self):
        self.response.payload = self.query()