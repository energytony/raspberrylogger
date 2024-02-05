#!/usr/bin/env python3
import minimalmodbus
import serial
import time
from timeloop import Timeloop
from datetime import timedelta
import json
import socket
import datetime
import redis
import time
 
from paho.mqtt import client as mqtt_client

 





redis_instance = redis.StrictRedis(host="localhost", port="6379", charset="utf-8", decode_responses=True,
                                   password="innovura_d84ser4xyz", db=0)
iot_host = socket.gethostname()
redis_key = 'raspberry'

print("MQTT Ping Program start ")

tl = Timeloop()





@tl.job(interval=timedelta(seconds=300))
def sample_job_every_300s():
    pingsystem()


 
def pingsystem():
    run()



def publish(client):
    
    try:
         
        topic = "datalogger/"+iot_host  # You might want to ensure `iot_host` is available globally or passed as a parameter
        time.sleep(1)
        msg = "PING "+datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print("Send Successful")
        else:
            print("Send Fail.!!!!")
    except Exception as e:
        print(f"Failed to publish message: {e}")
        time.sleep(5)  # Adding a wait time before potentially retrying
        pass
 
     
def run():
    try:
        client = connect_mqtt()
        if not (client==None):
            client.loop_start()
            publish(client)
            client.loop_stop()
    except (mqtt.MQTTException, TimeoutError) as e:
        print(f"An exception occurred: {e}")
        time.sleep(5)  # Wait for 5 seconds before trying to reconnect
        pass



def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt_client.MQTTv311, transport="tcp")        
    client.username_pw_set(username="innvoura", password="Q1w2e3r4t5")
    client.on_connect = on_connect
    print("Connecting...")
    try:
        client.connect("192.46.229.107", 1883, 60)
        return client
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        time.sleep(5)  # Wait before potentially retrying or taking other action
        return None  # Returning None to indicate that the connection was not successful

if __name__ == "__main__":
    

    time.sleep(1)
    tl.start(block=True)

