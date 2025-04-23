import minimalmodbus
from time import sleep

def read_wind_speed():
    try:
        mb_address = 7  # Modbus address for wind speed sensor
        sensor = minimalmodbus.Instrument('/dev/ttyUSB0', mb_address)

        sensor.serial.baudrate = 4800
        sensor.serial.bytesize = 8
        sensor.serial.parity = minimalmodbus.serial.PARITY_NONE
        sensor.serial.stopbits = 1
        sensor.serial.timeout = 0.5
        sensor.mode = minimalmodbus.MODE_RTU

        data = sensor.read_registers(0, 1, 3)  # Register 0x0000
        value = data[0] / 10.0
        print(f"Wind Speed = {value:.1f} m/s")

    except Exception as e:
        print("Wind Speed: Error -", e)

def read_wind_direction():
    try:
        mb_address = 6  # Modbus address for wind direction sensor
        sensor = minimalmodbus.Instrument('/dev/ttyUSB0', mb_address)

        sensor.serial.baudrate = 4800
        sensor.serial.bytesize = 8
        sensor.serial.parity = minimalmodbus.serial.PARITY_NONE
        sensor.serial.stopbits = 1
        sensor.serial.timeout = 0.5
        sensor.mode = minimalmodbus.MODE_RTU

        data = sensor.read_registers(1, 1, 3)  # Register 0x0001
        value = data[0] / 10.0
        print(f"Wind Direction = {value:.1f} °")

    except Exception as e:
        print("Wind Direction: Error -", e)

# Example usage
while True:
    read_wind_speed()
    read_wind_direction()
    sleep(3)
