import minimalmodbus
from time import sleep
from datetime import datetime
import csv

PORT = '/dev/ttyUSB0'
BAUDRATE = 4800
SCALE = 10.0
CSV_FILE = 'sensor_log.csv'

def create_instrument(address):
    sensor = minimalmodbus.Instrument(PORT, address)
    sensor.serial.baudrate = BAUDRATE
    sensor.serial.bytesize = 8
    sensor.serial.parity = minimalmodbus.serial.PARITY_NONE
    sensor.serial.stopbits = 1
    sensor.serial.timeout = 0.5
    sensor.mode = minimalmodbus.MODE_RTU
    return sensor

def read_register(address, register):
    try:
        sensor = create_instrument(address)
        value = sensor.read_register(register, 0, 3)
        return value / SCALE
    except Exception as e:
        print(f"Error reading addr {hex(address)} reg {hex(register)}: {e}")
        return None

def read_npk():
    try:
        sensor = create_instrument(0x01)
        nitrogen = sensor.read_register(0x0000, 0, 3)
        phosphorus = sensor.read_register(0x0002, 0, 3)
        potassium = sensor.read_register(0x0004, 0, 3)
        return nitrogen, phosphorus, potassium
    except Exception as e:
        print("NPK Sensor: Error -", e)
        return None, None, None

def log_to_csv(data):
    header = [
        "Timestamp", "Wind Speed (m/s)", "Wind Direction (°)", 
        "Leaf Humidity (%)", "Leaf Temp (°C)", 
        "Soil1 Moisture (%)", "Soil1 Temp (°C)",
        "Soil2 Moisture (%)", "Soil2 Temp (°C)", 
        "Illuminance (Lux)", "Louver Humidity (%)", "Louver Temp (°C)",
        "Nitrogen", "Phosphorus", "Potassium"
    ]
    write_header = False
    try:
        with open(CSV_FILE, 'r'):
            pass
    except FileNotFoundError:
        write_header = True

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(data)

while True:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    wind_speed = read_register(0x07, 0x0000)
    wind_direction = read_register(0x06, 0x0001)
    leaf_humidity = read_register(0x05, 0x0000)
    leaf_temp = read_register(0x05, 0x0001)

    soil1_moisture = read_register(0x03, 0x0000)
    soil1_temp = read_register(0x03, 0x0001)
    soil2_moisture = read_register(0x04, 0x0000)
    soil2_temp = read_register(0x04, 0x0001)

    illuminance = read_register(0x08, 0x0006)

    louver_humidity = read_register(0x09, 0x0000)
    louver_temp = read_register(0x09, 0x0001)

    nitrogen, phosphorus, potassium = read_npk()

    log_data = [
        timestamp, wind_speed, wind_direction,
        leaf_humidity, leaf_temp,
        soil1_moisture, soil1_temp,
        soil2_moisture, soil2_temp,
        illuminance, louver_humidity, louver_temp,
        nitrogen, phosphorus, potassium
    ]

    print(log_data)
    log_to_csv(log_data)

    sleep(5)
