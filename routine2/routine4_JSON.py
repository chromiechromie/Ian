myData = {1: 'Aragaki Yui', 2: 'GAKKI', 3: 'Nagasawa Masami'}
myData2 = {"1": "Aragaki Yui", "2": "GAKKI", "3": "Nagasawa Masami"}
import json
# dict to json
json_data = json.dumps(myData)
print(type(json_data))

#json to dict
dict_data = json.loads(json_data)
print(type(dict_data))

#class to json

class json_usage:
    def __init__(self,id,value):
        self.id = id
        self.value =value

def toJson(obj):
    return {
        'id':obj.id,
        'value':obj.value
    }

json_usage1 = json_usage(1,myData[2])
# print(json_usage1.id)
classToJSON = json.dumps(json_usage1,default=toJson)
# print(json.dumps(json_usage1,default=toJson))