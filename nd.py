import json
import urllib3

https = urllib3.PoolManager()
r = https.request('GET','https://www.kontests.net/api/v1/all')
dh = json.loads(r.data.decode('utf-8'))

for i in dh:
    print("{}  {}".format(i["in_24_hours"],i["site"]))
    
