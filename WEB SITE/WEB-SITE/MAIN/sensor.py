import mysql.connector
import RPi.GPIO as GPIO
import time

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="SensorData"
)
cursor = db.cursor()

GPIO.setmode(GPIO.BCM)

sensors = [
    {"name": "Temperature Sensor", "type": "DHT11", "pin": 4},
    {"name": "Light Sensor", "type": "LDR", "pin": 17}
]

for sensor in sensors:
    cursor.execute(
        "INSERT INTO Sensors (name, type, pin) VALUES (%s, %s, %s)",
        (sensor["name"], sensor["type"], sensor["pin"])
    )
    GPIO.setup(sensor["pin"], GPIO.IN)

db.commit()

def read_sensor_data(sensor):
    if sensor["type"] == "DHT11":
        value = 25.0  
    elif sensor["type"] == "LDR":
        value = GPIO.input(sensor["pin"]) * 100 
    else:
        value = 0.0
    return value

try:
    while True:
        for sensor in sensors:
            value = read_sensor_data(sensor)
            cursor.execute(
                "INSERT INTO SensorReadings (sensor_id, reading_value) VALUES (%s, %s)",
                (sensor["id"], value)
            )
        db.commit()
        time.sleep(5)  
except KeyboardInterrupt:
    print("Программа остановлена")
finally:
    GPIO.cleanup()
    cursor.close()
    db.close()