from geomet import wkt
import requests
import base64
import json

url = "http://158.49.112.122:7474/db/data/transaction/commit"
headers = { "Authorization": 'Basic ' + base64.b64encode('Smart:Politech'.encode('utf-8')).decode("utf-8"),
    "X-Stream": "true",
    "Accept": "application/json; charset=UTF-8",
    "Content-Type": "application/json"}


statement = "match (n) return n"
data = { "statements": [{"statement": statement ,"resultDataContents": ["row", "graph", "rest"]}]}
response = requests.post(url, 
            data=json.dumps(data),
            headers=headers)


statement_out = "match (n) where n.id = '{}' set n+= {{ wkt: '{}' }};"

json_data = json.loads(response.content)["results"][0]["data"]
for i in json_data:
    row = i["row"][0]
    if row.get("wkt") is None and row.get("geojson") is not None:
        geojson = json.loads(row.get("geojson"))["features"][0]["geometry"]
        w = wkt.dumps(geojson, decimals= 8)
        query = statement_out.format(row["id"], w)
        print(query) 
        data = { "statements": [{"statement": query ,"resultDataContents": ["row", "graph", "rest"]}]}

        response = requests.post(url, 
            data=json.dumps(data),
            headers=headers)

