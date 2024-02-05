import serial
import re

 
import time
from datetime import timedelta
import json
import socket
import datetime
import redis
import time
from paho.mqtt import client as mqtt_client
redis_instance = redis.StrictRedis(host="localhost",port="6379", charset="utf-8", decode_responses=True ,password="innovura_d84ser4xyz" , db=0)
iot_host = socket.gethostname()
redis_key='raspberry'
indexkey=0
qot_id="78"

# Define the serial port and baud rate.
# Ensure the 'COM#' is set to the port to which your Arduino is connected.
# For Linux, it might be something like "/dev/ttyACM0" or "/dev/ttyUSB0".
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600


def extract_data(s):
    pattern = r'\[\d+(?:,\d+)*\]'

    match = re.search(pattern, s)
    
    if match:
        return match.group(0), True
    else:
        return None, False


def extract_ping(s):
    ping_pattern = r'\{"PING":"0","iot_id": "([^"]+)"\}'


    match = re.search(ping_pattern, s)
    
    if match:
        return match.group(1), True
    else:
        return None, False

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()



def read_from_port(port):
    serial_port = serial.Serial(port, BAUD_RATE, timeout=1)
    global qot_id
    try:
        while True:
            if serial_port.in_waiting:
                try:
                    line = serial_port.readline().decode('utf-8').strip()
                except UnicodeDecodeError as e:
                # Handle the decoding error (e.g., print an error message)
                    print(f"UnicodeDecodeError: {e}")
                    # Optionally, you can continue reading from the serial port
                    continue

                data, data_is_valid = extract_data(line)

                ping, ping_is_valid = extract_ping(line)

                if(data_is_valid):
                    print("Data is :")
                     
                    write_to_redis(data)
                if(ping_is_valid):
                    print("Received QOT ID is :")
                    qot_id=ping
                   
                    pingsystem( )

    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        serial_port.close()


def write_to_redis(input_string):
    data = {}
     
    labels = ["Voltage A", "Voltage B", "Voltage C", "Current A", "Current B", "Current C", "PF A", "PF B", "PF C", "KWH"]

  
    data['slavid_id'] = "1"
    data['lora_id'] = "1"
    data['iot_host'] = iot_host
    data['time'] = datetime.datetime.utcnow()
    items = input_string.strip('[]').split(',')
    
    for label, item in zip(labels, items):
        data[label] = int(item) 
    
   

    print(data)
    json_input = json.dumps(data, default=myconverter)
    redis_instance.lpush(redis_key, json_input)
   
  


def pingsystem( ):
    run( )



def publish(client ):
    global qot_id 
   
    no_spaces_string = qot_id[:10]
  
    topic = "QOT/"+ no_spaces_string
    time.sleep(1)
 
    msg = " PING "+datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    result = client.publish(topic, msg)
   
    status = result[0]
    if status == 0:
        print("Send Successful  : "+msg +" " + topic)
    else:
        print("Send Fail.!!!!")
 
     
def run():
    try:
        client = connect_mqtt()
        if client is not None:
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
    try:
        client = mqtt_client.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt_client.MQTTv311, transport="tcp")        
        client.username_pw_set(username="innvoura", password="Q1w2e3r4t5")
        client.on_connect = on_connect
        print("Connecting...")
        client.connect("192.46.229.107", 1883, 60)

        return client
    except ConnectionRefusedError:
        print("Connection to MQTT broker refused. Check the host and port.")
        pass
    except TimeoutError:
        print("Connection to MQTT broker timed out. Check your internet connection.")
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pass

    return None



if __name__ == "__main__":
    print("Modbus-Lora Program start ")
    read_from_port(SERIAL_PORT)
 