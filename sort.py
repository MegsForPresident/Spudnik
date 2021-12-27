import json

data = {}
with open('Users.json','r') as f:
    data = json.load(f)
daTa = {}
datData = sorted(data)
for key in datData:
    daTa[key] = data[key]
with open('Users.json','w') as f:
    json.dump(daTa,f,indent=5)