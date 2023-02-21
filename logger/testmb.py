#!/usr/bin/env python3
import minimalmodbus
import serial

slave_instrument = ""

slave_instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
print("Test 1")
slave_instrument.serial.baudrate = 19200
slave_instrument.serial.bytesize = 8
slave_instrument.serial.parity = serial.PARITY_EVEN
slave_instrument.serial.stopbits = 1
slave_instrument.serial.timeout = 5

try:
    print(slave_instrument)
    print(slave_instrument.read_float(0,functioncode=3,number_of_registers=2))
except IOError:
    print("Failed to read from instrument")

print("Test 2")
slave_instrument.serial.baudrate = 19200
slave_instrument.serial.bytesize = 8
slave_instrument.serial.parity = serial.PARITY_ODD
slave_instrument.serial.stopbits = 1
slave_instrument.serial.timeout = 5

try:
    print(slave_instrument)
    print(slave_instrument.read_float(0,functioncode=3,number_of_registers=2))
except IOError:
    print("Failed to read from instrument")    

print("Test 3")
slave_instrument.serial.baudrate = 19200
slave_instrument.serial.bytesize = 8
slave_instrument.serial.parity = serial.PARITY_NONE
slave_instrument.serial.stopbits = 1
slave_instrument.serial.timeout = 5

try:
    print(slave_instrument)
    print(slave_instrument.read_float(0,functioncode=3,number_of_registers=2))
except IOError:
    print("Failed to read from instrument")    

print("Test 4")
slave_instrument.serial.baudrate = 9600
slave_instrument.serial.bytesize = 8
slave_instrument.serial.parity = serial.PARITY_EVEN
slave_instrument.serial.stopbits = 1
slave_instrument.serial.timeout = 5

try:
    print(slave_instrument)
    print(slave_instrument.read_float(0,functioncode=3,number_of_registers=2))
except IOError:
    print("Failed to read from instrument")    

print("Test 5")
slave_instrument.serial.baudrate = 19200
slave_instrument.serial.bytesize = 8
slave_instrument.serial.parity = serial.PARITY_EVEN
slave_instrument.serial.stopbits = 1
slave_instrument.serial.timeout = 5

try:
    print(slave_instrument)
    print(slave_instrument.read_float(0,functioncode=3,number_of_registers=2))
except IOError:
    print("Failed to read from instrument")    


print("Test 6")
slave_instrument.serial.baudrate = 9600
slave_instrument.serial.bytesize = 8
slave_instrument.serial.parity = serial.PARITY_NONE
slave_instrument.serial.stopbits = 1
slave_instrument.serial.timeout = 5

try:
    print(slave_instrument)
    print(slave_instrument.read_float(0,functioncode=3,number_of_registers=2))
except IOError:
    print("Failed to read from instrument")    

print("Test 7")
slave_instrument.serial.baudrate = 9600
slave_instrument.serial.bytesize = 8
slave_instrument.serial.parity = serial.PARITY_ODD
slave_instrument.serial.stopbits = 1
slave_instrument.serial.timeout = 5

try:
    print(slave_instrument)
    print(slave_instrument.read_float(0,functioncode=3,number_of_registers=2))
except IOError:
    print("Failed to read from instrument")    




