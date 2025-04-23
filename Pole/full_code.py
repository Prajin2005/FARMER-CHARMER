import minimalmodbus
from time import sleep

def init_sensor(mb_address):
    sensor = minimalmodbus.Instrument('/dev/ttyUSB0', mb_address)
    sensor.serial.baudrate = 4800
    sensor.serial.bytesize = 8
    sensor.serial.parity = minimalmodbus.serial.PARITY_NONE
    sensor.serial.stopbits = 1
    sensor.serial.timeout = 0.5
    sensor.mode = minimalmodbus.MODE_RTU
    return sensor

def read_scaled_register(sensor, register, label, unit, scale=10.0):
    try:
        data = sensor.read_registers(register, 1, 3)
        value = data[0] / scale
        print(f"{label} = {value:.1f}{unit}")
    except Exception as e:
        print(f"{label}: Error -", e)

def read_soil_moisture1():
    sensor = init_sensor(3)
    read_scaled_register(sensor, 0, "Soil Moisture 1", " %")

def read_soil_moisture2():
    sensor = init_sensor(4)
    read_scaled_register(sensor, 0, "Soil Moisture 2", " %")

def read_leaf_moisture():
    sensor = init_sensor(5)
    read_scaled_register(sensor, 0, "Leaf Moisture", " %")

def read_wind_direction():
    sensor = init_sensor(6)
    read_scaled_register(sensor, 1, "Wind Direction", " °")

def read_wind_speed():
    sensor = init_sensor(7)
    read_scaled_register(sensor, 0, "Wind Speed", " m/s")

def read_lux():
    sensor = init_sensor(8)
    read_scaled_register(sensor, 0, "LUX", " lx")

def read_temp_and_humidity():
    sensor = init_sensor(9)
    try:
        data = sensor.read_registers(0, 2, 3)  # Temp at 0, Humidity at 1
        temp = data[0] / 10.0
        humidity = data[1] / 10.0
        print(f"Temperature = {temp:.1f} °C")
        print(f"Humidity = {humidity:.1f} %")
    except Exception as e:
        print("Temp and Humidity: Error -", e)

def read_npk():
    try:
        sensor = init_sensor(1)  # NPK sensor address
        nitrogen = sensor.read_register(0x0000, 0, 3)
        phosphorus = sensor.read_register(0x0002, 0, 3)
        potassium = sensor.read_register(0x0004, 0, 3)
        print(f"Nitrogen = {nitrogen} mg/kg")
        print(f"Phosphorus = {phosphorus} mg/kg")
        print(f"Potassium = {potassium} mg/kg")
    except Exception as e:
        print("NPK Sensor: Error -", e)

# Example usage
while True:
    read_soil_moisture1()
    read_soil_moisture2()
    read_leaf_moisture()
    read_wind_speed()
    read_wind_direction()
    read_lux()
    read_temp_and_humidity()
    read_npk()
    print("-" * 40)
    sleep(3)
