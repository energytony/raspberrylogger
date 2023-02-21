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

    for register_address in range(0, 18):
        if (register_address % 2) == 0:
            value = slave_instrument.read_long(registeraddress=register_address,
                                           functioncode=3, signed=False)
            print("the value in the register with the address {} is {} ".format(register_address, value))

except:
    print("there is problem in reading the values")
