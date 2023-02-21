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

redis_instance = redis.StrictRedis(host="localhost",port="6379", charset="utf-8", decode_responses=True ,password="innovura_d84ser4xyz" , db=0)
iot_host = socket.gethostname()
redis_key='raspberry'


print("Modbus Program start ")


tl = Timeloop()

def DeviceFileCheck(fn):
    global device_data

    try:
    	
    	with open(fn) as json_file:
    		device_data = json.load(json_file)
    		
    	return 1
    except IOError:
    	print ("Error: Device Json does not appear to exist.")
    	return 0

def SettingFileCheck(fn):
	global setting_data
	try:

		with open(fn) as json_file:
			setting_data = json.load(json_file)

		return 1
	except IOError:
		print ("Error: Setting Json does not appear to exist.")
		return 0

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()





	
			
@tl.job(interval=timedelta(seconds=15))
def sample_job_every_15s():
    data= {}

    print("15s job current time : {}".format(time.ctime()))

    for d in range(len(device_data["device"])):
	    data['slavid_id'] = device_data["device"][d]['slave_address']
	    data['lora_id'] = device_data["device"][d]['slave_address']
	    data['iot_host'] = iot_host
	    data['time'] = datetime.datetime.utcnow()

	    for i in range(len(setting_data["field"])):
	    	fieldname = setting_data["field"][i]["name"]
	    	datatype = setting_data["field"][i]["type_of_value"]
	    	value = instrument[d].read_long(setting_data["field"][i]["start_registers_address"], functioncode=3, signed=True, byteorder=0)
	    	#value = instrument[d].read_float(registeraddress=setting_data["field"][i]["start_registers_address"],functioncode=3,number_of_registers=2)
	    	data[fieldname] = value
	    	

	    print(data)
	    json_input = json.dumps(data ,default = myconverter)
	    redis_instance.lpush(redis_key, json_input)

    







if __name__ == "__main__":
	result = DeviceFileCheck("devicem.json")
	
	#result = SettingFileCheck("setting-ex.json")
	#result = SettingFileCheck("setting.json")
	#result = SettingFileCheck("setting-china.json")
	result = SettingFileCheck("setting-C10.json")
	#result = SettingFileCheck("setting-CVMK2.json")
	#result = SettingFileCheck("setting-AC2.json")
	#result = SettingFileCheck("setting-PM5000.json")
	#result = SettingFileCheck("setting-C1000.json")
		
	instrument= {}	

	time.sleep(1)
	if (result):
		#instrument = minimalmodbus.Instrument('/dev/ttyUSB0', device_data['slave_address'])
		#instrument.serial.baudrate = device_data['setting']['baudrate']
		#instrument.serial.bytesize = device_[i]data['setting']['bytesize']
		#instrument.serial.parity   = serial.[i]PARITY_EVEN
		#instrument.serial.stopbits = device_data['setting']['stopbits']
		#instrument.serial.timeout  = device_[i]data['setting']['timeout']
 

		for i in range(len(device_data["device"])):
			
			instrument[i] = minimalmodbus.Instrument('/dev/ttyUSB0', device_data["device"][i]['slave_address'])
			instrument[i].serial.baudrate = device_data["device"][i]['setting']['baudrate']
			instrument[i].serial.bytesize = device_data["device"][i]['setting']['bytesize']
			instrument[i].serial.parity   = serial.PARITY_EVEN
			instrument[i].serial.stopbits = device_data["device"][i]['setting']['stopbits']
			instrument[i].serial.timeout  = device_data["device"][i]['setting']['timeout']
			
			
		tl.start(block=True)
	
