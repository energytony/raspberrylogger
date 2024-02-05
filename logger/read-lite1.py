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


@tl.job(interval=timedelta(seconds=15))
def sample_job_every_15s():
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
            #value = instrument.read_long(setting_data["field"][i]["start_registers_address"], functioncode=3,signed=True, byteorder=0)
            value = instrument.read_float(registeraddress=setting_data["field"][i]["start_registers_address"],functioncode=4,number_of_registers=2)
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


if __name__ == "__main__":
    result = DeviceFileCheck("device1.json")
    #result = DeviceFileCheck("device-solar.json")

    #result = SettingFileCheck("setting.json")
    result = SettingFileCheck("setting-china.json")
    #result = SettingFileCheck("setting-C10.json")
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
        tl.start(block=True)

