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

print("Modbus Program start ")

tl = Timeloop()

indexkey=0

def DeviceFileCheck(fn):
    global device_data

    try:

        with open(fn) as json_file:
            device_data = json.load(json_file)

        return 1
    except IOError:
        print("Error: Device Json does not appear to exist.")
        return 0


def SettingFileCheck(fn):
    global setting_data
    try:

        with open(fn) as json_file:
            setting_data = json.load(json_file)

        return 1
    except IOError:
        print("Error: Setting Json does not appear to exist.")
        return 0


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()


@tl.job(interval=timedelta(seconds=15))
def sample_job_every_15s():
    global indexkey 
    data = {}
    flag = 0
    print("15s job current time : {}".format(time.ctime()))
    # print(time.strftime("%H:%M:%S", time.localtime()))
    # address=0
    # voltage_phase = instrument.read_long(address, functioncode=3, signed=True, byteorder=0)
    # print("Value {}".format(voltage_phase))
    data['slavid_id'] = device_data['slave_address']
    data['lora_id'] = device_data['slave_address']
    data['iot_host'] = iot_host
    data['time'] = datetime.datetime.utcnow()

    for i in range(len(setting_data["field"])):
        fieldname = setting_data["field"][i]["name"]
        datatype = setting_data["field"][i]["type_of_value"]
        
        try:
            value = instrument.read_long(setting_data["field"][i]["start_registers_address"], functioncode=3,signed=True, byteorder=0)
            #value = instrument.read_float(registeraddress=setting_data["field"][i]["start_registers_address"],functioncode=4,number_of_registers=2)
            #value = instrument.read_register(registeraddress=setting_data["field"][i]["start_registers_address"],functioncode=3,number_of_decimals=0,signed=True)
            value = str(round(value, 2))
        # data[fieldname] = value
        except Exception as e:
            print("[!] Exception occurred: ", e)
            flag = 1
        else:
            data[fieldname] = float(value)
            flag = 0

    if (flag == 0):
        print(data)
        json_input = json.dumps(data, default=myconverter)
        redis_instance.lpush(redis_key, json_input)
        indexkey = indexkey +1
        print (indexkey)
        if (indexkey >19):
            pingsystem()
            indexkey=1


 
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
    result = DeviceFileCheck("device.json")
    #result = DeviceFileCheck("device-solar.json")

    #result = SettingFileCheck("setting.json")
    #result = SettingFileCheck("setting-china.json")
    result = SettingFileCheck("setting-C10.json")
    #result = SettingFileCheck("setting-CVMK2.json")
    # result = SettingFileCheck("setting-AC2.json")
    # result = SettingFileCheck("setting-PM5000.json")
    # result = SettingFileCheck("setting-C1000.json")
    #result = SettingFileCheck("setting-solar.json")
    #result = SettingFileCheck("setting-china2.json")

    
    


    time.sleep(1)
    if (result):
        instrument = minimalmodbus.Instrument('/dev/ttyUSB0', device_data['slave_address'])
        instrument.serial.baudrate = device_data['setting']['baudrate']
        instrument.serial.bytesize = device_data['setting']['bytesize']
        instrument.serial.parity = device_data['setting']['parity']
        instrument.serial.stopbits = device_data['setting']['stopbits']
        instrument.serial.timeout = device_data['setting']['timeout']
        # print(len(device_data))
        #print(instrument)
        #run()
        tl.start(block=True)

