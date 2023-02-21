import json
import time , threading
from datetime import datetime
import socket
iot_host = "raspberry-133"
import requests
url = 'http://192.46.225.215:8080'
headers = {"content-type : ": "application/json"}
import random
import paho.mqtt.client as mqtt


def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)



def pushdata(inputjson):
    my_json = inputjson.decode('utf8').replace("'", '"')
    data_dict = json.loads(my_json)
    print(data_dict["distance"])

    datajson = {}
    n = random.random()*6
    print(n)
    now = datetime.now()
    datajson['iot_host'] = iot_host
    datajson['time'] = now.isoformat()
    datajson['iot_id'] = data_dict["lorasensor"]
    datajson['distance'] = data_dict["distance"]
    datajson['battery'] = data_dict["battery"]

    if(int(datajson['distance'])>14):
        datajson['usage'] =0
    else:
        a= (15-int(datajson['distance']))/13
        a=truncate(a,2)
        datajson['usage'] =a
    

    print(datajson)
    response = requests.post(url, json=datajson, auth=('logstash', 'iottest'))
    print("Server responded with %s" % response.status_code)
    

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("lora/gateway/toilet")

def on_message(client, userdata, msg):
    #print(msg.topic, msg.payload)
    pushdata(msg.payload)


client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
client.on_connect = on_connect
client.on_message = on_message



client.username_pw_set(username="innvoura", password="Q1w2e3r4t5")
print("Connecting...")
client.connect("192.46.229.107", 1883, 10)
client.loop_forever()