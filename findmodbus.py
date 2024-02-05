import minimalmodbus
import serial

def probe_modbus_device(serial_port):
    # List of standard baud rates to try
    BAUD_RATES = [9600, 19200, 38400,115200]

    # Probe baud rates
    for baud_rate in BAUD_RATES:
        for slave_address in range(1, 248):  # Valid Modbus addresses are 1-247
            try:
                instrument = minimalmodbus.Instrument(serial_port, slave_address)
                instrument.serial.baudrate = baud_rate
                instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
                instrument.serial.stopbits = 1
                instrument.serial.timeout = 0.05

                # Try reading a register to see if the device responds
                value = instrument.read_register(0)  # Trying with register 0 as a starting point
                print(f"Found device at slave address {slave_address} with baud rate {baud_rate}")
                return baud_rate, slave_address

            except (minimalmodbus.NoResponseError, serial.SerialException):
                continue  # Try next configuration

    print("Unable to determine Modbus device configuration.")
    return None, None

if __name__ == "__main__":
    print("Testing ")
    baud_rate, slave_address = probe_modbus_device('/dev/ttyUSB0')
    if baud_rate and slave_address:
        print(f"Device configuration: Baud Rate = {baud_rate}, Slave Address = {slave_address}")
    else:
        print("Failed to detect device configuration.")
