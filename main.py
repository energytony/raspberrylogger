import json
import time , threading
from datetime import datetime
import socket
iot_host = "raspberry-133"
import requests
url = 'http://192.46.225.215:8080'
headers = {"content-type : ": "application/json"}
import random
xvalue =5
xvalue1 =11
xvalue2 =6
xvalue3 =9
xbattery =3000

def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)

def pushdata1():
    datajson = {}
    n = random.random()*3
    print(n)
    global xvalue
    global xbattery
    now = datetime.now()
    datajson['iot_host'] = iot_host
    datajson['time'] = now.isoformat()
    datajson['iot_id'] = "101"
    datajson['distance'] = truncate(xvalue -(n),1)
    datajson['battery'] = truncate(xbattery-(n),1)


  
    if(int(datajson['distance'])>14):
        datajson['usage'] =0
    else:
        a= (15-int(datajson['distance']))/13
        a=truncate(a,2)
        datajson['usage'] =a
    
    print(datajson)
    response = requests.post(url, json=datajson, auth=('logstash', 'iottest'))
    print("Server responded with %s" % response.status_code)
    time.sleep(10)

def pushdata2():
    datajson = {}
    n = random.random()*5
    print(n)
    global xvalue
    global xbattery
    now = datetime.now()
    datajson['iot_host'] = iot_host
    datajson['time'] = now.isoformat()
    datajson['iot_id'] = "102"
    datajson['distance'] = truncate(xvalue1-(n),1)
    datajson['battery'] = truncate(xbattery-(n),1)


    if(int(datajson['distance'])>14):
        datajson['usage'] =0
    else:
        a= (15-int(datajson['distance']))/13
        a=truncate(a,2)
        datajson['usage'] =a
    

    print(datajson)
    response = requests.post(url, json=datajson, auth=('logstash', 'iottest'))
    print("Server responded with %s" % response.status_code)
    time.sleep(10)

def pushdata3():
    datajson = {}
    n = random.random()*8
    print(n)
    global xvalue
    global xbattery
    now = datetime.now()
    datajson['iot_host'] = iot_host
    datajson['time'] = now.isoformat()
    datajson['iot_id'] = "103"
    datajson['distance'] = truncate(xvalue2-(n),1)
    datajson['battery'] = truncate(xbattery-(n),1)


    if(int(datajson['distance'])>14):
        datajson['usage'] =0
    else:
        a= (15-int(datajson['distance']))/13
        a=truncate(a,2)
        datajson['usage'] =a
    
    print(datajson)
    response = requests.post(url, json=datajson, auth=('logstash', 'iottest'))
    print("Server responded with %s" % response.status_code)
    time.sleep(10)


def pushdata4():
    datajson = {}
    n = random.random()*6
    print(n)
    global xvalue
    global xbattery
    now = datetime.now()
    datajson['iot_host'] = iot_host
    datajson['time'] = now.isoformat()
    datajson['iot_id'] = "104"
    datajson['distance'] = truncate(xvalue3-(n),1)
    datajson['battery'] = truncate(xbattery-(n),1)


    if(int(datajson['distance'])>14):
        datajson['usage'] =0
    else:
        a= (15-int(datajson['distance']))/13
        a=truncate(a,2)
        datajson['usage'] =a
    
    print(datajson)
    response = requests.post(url, json=datajson, auth=('logstash', 'iottest'))
    print("Server responded with %s" % response.status_code)
    time.sleep(10)
while True:
  pushdata1()
  pushdata2()
  pushdata3()
  pushdata4()


  time.sleep(120)

