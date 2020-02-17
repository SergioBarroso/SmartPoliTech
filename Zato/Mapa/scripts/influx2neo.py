import requests
from influxdb import InfluxDBClient
import json 
import datetime
import base64
import numpy as np


client = InfluxDBClient(
        host='10.253.247.18', port=8086, username='r0b0l4b', password='alwayssmarter4')
a = client.get_list_database()
print(a)
print(client.ping())
client.switch_database('sensors')
influx_sensors = np.array([x["name"] for x in client.get_list_measurements()])
print("influx\n",influx_sensors)


url = "http://158.49.112.122:7474/db/data/transaction/commit"
headers = { "Authorization": 'Basic ' + base64.b64encode('Smart:Politech'.encode('utf-8')).decode("utf-8"),
    "X-Stream": "true",
    "Accept": "application/json; charset=UTF-8",
    "Content-Type": "application/json"}



statement = "match (n:Device) return n.id"
data = { "statements": [{"statement": statement ,"resultDataContents": [ "row"]}]}
response = requests.post(url, 
            data=json.dumps(data),
            headers=headers)
json_data = json.loads(response.content)["results"][0]["data"]
neo4j_sensors = np.array([x["row"][0] for x in json_data])
print("neo4j\n", neo4j_sensors)

diff = np.setdiff1d(influx_sensors, neo4j_sensors)
print("\n diff \n", diff)

sensor = {
    "geojeson" : "",
    "img" : "",
    "wkt": "",
    "type": "",
    "min_zoom" : 21,
    "max_zoom" : 50,
    "gtype": 1,
    "id": "",
    "description" : "",
    "dataSource" : "",
    "bbox" : "",
    "name" : ""
}