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
previous_logger_state = None 

redis_instance = redis.StrictRedis(host="localhost", port="6379", charset="utf-8", decode_responses=True,
                                   password="innovura_d84ser4xyz", db=0)
iot_host = socket.gethostname()
redis_key = 'raspberry'

print("Modbus Program start ")

tl = Timeloop()


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

def initialize_instrument():
    # Function to initialize the instrument with the latest settings
    global instrument  # Make sure to use the global keyword if 'instrument' is a global variable
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', int(redis_instance.get(f'slaveId')))
    instrument.serial.baudrate = int(redis_instance.get(f'baudRate'))
    instrument.serial.bytesize = device_data['setting']['bytesize']
    instrument.serial.parity = redis_instance.get(f'parity')
    instrument.serial.stopbits = device_data['setting']['stopbits']
    instrument.serial.timeout = device_data['setting']['timeout']
    print(instrument)


@tl.job(interval=timedelta(seconds=15))
def sample_job_every_15s():
    global previous_logger_state  # Use the global variable

    current_logger_state = redis_instance.get(f'logger')

    if current_logger_state == "ON":
        if previous_logger_state != "ON":
            # Logger state changed from OFF to ON, reinitialize instrument settings
            initialize_instrument()
            
        print("logger start")
        redis_instance.set(f'loggermessage', " Running..")
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
                redis_instance.set(f'loggermessage', str(e))
                flag = 1
                redis_instance.set(f'loggermessage', " Stop..")
            else:
                data[fieldname] = float(value)
                flag = 0
    else:
        # Logger state is OFF, handle accordingly
        flag = 1
        redis_instance.set(f'loggermessage', " Stop..")      

       
    if (flag == 0):
        print(data)
        json_input = json.dumps(data, default=myconverter)
        redis_instance.lpush(redis_key, json_input)
 
   
    previous_logger_state = redis_instance.get(f'logger')


def get_file_for_setting(setting_index):
    setting_files = {
        1: "setting-C10.json",
        2: "setting.json",
        3: "setting-china.json",  # Example names, replace with actual file names
        4: "setting-PM5000.json",
        5: "setting-westbill",
        6: "setting-umg96s",
        7: "setting-umg508",
        8: "setting-PM5000.json"
    }

    file_name = setting_files.get(setting_index)
    redis_instance.set(f'setting_name' ,  str(file_name))
    if file_name:
        return SettingFileCheck(file_name)
    else:
        raise ValueError("Invalid setting index")

if __name__ == "__main__":
    
    setting_index = redis_instance.get(f'setting')
    print (setting_index)


    result = DeviceFileCheck("device.json")
 
    result = get_file_for_setting(int(setting_index))
 
    print (redis_instance.get(f'slaveId'))
    print (redis_instance.get(f'baudRate'))
    print (redis_instance.get(f'parity') )
    time.sleep(1)
    if (result):
        instrument = minimalmodbus.Instrument('/dev/ttyUSB0', int(redis_instance.get(f'slaveId')))
        instrument.serial.baudrate = redis_instance.get(f'baudRate')
        instrument.serial.bytesize = device_data['setting']['bytesize']
        instrument.serial.parity =  redis_instance.get(f'parity')
        instrument.serial.stopbits = device_data['setting']['stopbits']
        instrument.serial.timeout = device_data['setting']['timeout']
        # print(len(device_data))
        print(instrument)
        tl.start(block=True)

