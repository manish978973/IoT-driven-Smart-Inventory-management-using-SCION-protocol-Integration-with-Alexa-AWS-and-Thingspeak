#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import mysql.connector
from mfrc522 import SimpleMFRC522
import socket
import json
import Adafruit_DHT

continue_reading = True

sensor_name = Adafruit_DHT.DHT11
sensor_pin = 17


db = mysql.connector.connect(
  host="localhost",
  user="productadmin",
  passwd="raspberry",
  database="productinfo"
)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0',2235))
sock.listen(1)

cursor = db.cursor()
reader = SimpleMFRC522()

while True:
    c ,addr = sock.accept()
    while True:
        data = c.recv(128)
        humidity, temperature = Adafruit_DHT.read_retry(sensor_name, sensor_pin)
       
        try:
            if(continue_reading):
                id, text = reader.read()
                cursor.execute("SELECT * FROM products WHERE rfid_uid="+str(id))
                records = cursor.fetchall()
                if cursor.rowcount >= 1:
                    for row in records:
                        x = {"Name":row[2],"UnitWeight":row[3],"Humidity":humidity,"Temperature":temperature}
                        y = json.dumps(x)
                        print(y)

                else:
                     print("Card not Registered")
          

                db.commit()
                c.send(y.encode())
                if not data:
                    c.close()
                    break
                #time.sleep(1);

        finally:
            GPIO.cleanup()
