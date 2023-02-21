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
import sx126x

import time
import sys
sys.path.append('./drive')
import SPI
import SSD1305

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

RST = None   

DC = 24
SPI_PORT = 0
SPI_DEVICE = 0

redis_instance = redis.StrictRedis(host="localhost",port="6379", charset="utf-8", decode_responses=True ,password="innovura_d84ser4xyz" , db=0)
iot_host = socket.gethostname()
redis_key='raspberry'
disp = SSD1305.SSD1305_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

node = sx126x.sx126x(serial_num = "/dev/ttyS0",freq=433,addr=21,power=22,rssi=True)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = 0
top = padding
bottom = height-padding
x = 0


font = ImageFont.truetype('04B_08__.TTF',8)
print("OLED start ")


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
    print(time.strftime("%H:%M:%S", time.localtime()))
    #address=0
    #voltage_phase = instrument.read_long(address, functioncode=3, signed=True, byteorder=0)
    #print("Value {}".format(voltage_phase))
    #data['slavid_id'] = device_data['slave_address']
    data['lora_id'] = device_data['slave_address']
    #data['iot_host'] = iot_host
    #data['time'] = datetime.datetime.utcnow()

    for i in range(len(setting_data["field"])):
    	fieldname = setting_data["field"][i]["name"]
    	datatype = setting_data["field"][i]["type_of_value"]
    	##value = instrument.read_float(setting_data["field"][i]["start_registers_address"], functioncode=4, number_of_registers=2, byteorder=0)
    	value = instrument.read_long(setting_data["field"][i]["start_registers_address"], functioncode=3, signed=True, byteorder=0)
    	data[fieldname] = value
    	
    node.addr_temp = 21
    node.set(node.freq,node.addr_temp,node.power,node.rssi)
   
    print(data)
    json_input = json.dumps(data ,default = myconverter)
    redis_instance.lpush(redis_key, json_input)

    node.send(json_input)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top),"Node: " + str(data['lora_id']) +" "+str(time.strftime("%H:%M:%S", time.localtime())) ,  font=font, fill=255)
    draw.text((x, top+8),"V1: " + str(data["Voltage A"]) + "  L1: "+ str(data["Current A"]) ,  font=font, fill=255)
    draw.text((x, top+16),"V2: " + str(data["Voltage B"]) + "  L2: "+ str(data["Current B"]) ,  font=font, fill=255)
    draw.text((x, top+25),"V3: " + str(data["Voltage C"]) + "  L3: "+ str(data["Current C"]) ,  font=font, fill=255)
    disp.image(image)
    disp.display()








if __name__ == "__main__":
	result = DeviceFileCheck("device.json")
	
	result = SettingFileCheck("setting-C10.json")
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	if(result):
		draw.text((x, top),"Config file read Success !" ,  font=font, fill=255)
	else:
		draw.text((x, top),"Config file Error !!" ,  font=font, fill=255)
	draw.text((x, top+8),str(node) ,  font=font, fill=255)
	#draw.text((x, top+16),str(node) ,  font=font, fill=255)
	draw.text((x, top+25),str(redis_instance) ,  font=font, fill=255)

	disp.image(image)
	disp.display()
	

	time.sleep(1)
	if (result):
		instrument = minimalmodbus.Instrument('/dev/ttyUSB0', device_data['slave_address'])
		instrument.serial.baudrate = device_data['setting']['baudrate']
		instrument.serial.bytesize = device_data['setting']['bytesize']
		instrument.serial.parity   = serial.PARITY_EVEN
		instrument.serial.stopbits = device_data['setting']['stopbits']
		instrument.serial.timeout  = device_data['setting']['timeout']
		#print(len(device_data))
		
		tl.start(block=True)
	
