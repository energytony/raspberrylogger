#!/usr/bin/env python3
import minimalmodbus
import serial

slave_instrument = ""
try:
    slave_instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)

    print()
    slave_instrument.serial.baudrate = 19200
    slave_instrument.serial.bytesize = 8
    slave_instrument.serial.parity = serial.PARITY_EVEN
    slave_instrument.serial.stopbits = 1
    slave_instrument.serial.timeout = 0.05

    for register_address in range(30, 40):
        #if (register_address % 2) == 0:
        #value = slave_instrument.read_long(registeraddress=register_address,functioncode=3, signed=False)
        value = slave_instrument.read_float(registeraddress=register_address,functioncode=3,number_of_registers=2)
        #value = slave_instrument.read_register(registeraddress=register_address,functioncode=3,number_of_decimals=0,signed=True)
        print("the value in the float with the address {} is {} ".format(register_address, value))


    for register_address in range(30, 40):
        #if (register_address % 2) == 0:
        #value = slave_instrument.read_long(registeraddress=register_address,functioncode=3, signed=False)
        value = slave_instrument.read_register(registeraddress=register_address,functioncode=3,number_of_decimals=0,signed=True)
        print("the value in the register with the address {} is {} ".format(register_address, value))


    for register_address in range(30, 40):
        #if (register_address % 2) == 0:
        value = slave_instrument.read_float(registeraddress=register_address,functioncode=3,number_of_registers=2)
        print("the value in the FLOAT with the address {} is {} ".format(register_address, value))

except:
    print("there is problem in reading the values")
