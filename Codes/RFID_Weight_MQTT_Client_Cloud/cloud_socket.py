#! /usr/bin/python3
import RPi.GPIO as GPIO
import socket
import json
import time
import sys
import paho.mqtt.client as paho
import urllib.request


myAPI = 'N5D2CEV26WIRWUDR'
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

broker="192.168.0.101"
port=1883

client1= paho.Client("control1")
client1.connect(broker,port)

EMULATE_HX711=False
referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711


def cleanAndExit():
    #print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    #print("Bye!")
    sys.exit()


import math
def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)




hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(-2134)

hx.reset()
hx.tare()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 2235))
a = "I am Client"

try:
    while True:
        try:
            client.send(a.encode())
            val = max(0, int(hx.get_weight(5)))
            #print(val)
            from_server = json.loads(client.recv(4096).decode())
            quantity = normal_round(int(val) / int(from_server['UnitWeight']))
            jobject = {'Name':from_server['Name'],'UnitWeight':from_server['UnitWeight'],'TotalWeight':val,'Quantity':quantity,'Humidity':from_server['Humidity'],'Temperature':from_server['Temperature']}
            a = json.dumps(jobject)
            print(a)
            client1.publish("productinfo",a)
            conn = urllib.request.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s' % (from_server['Name'], str(from_server['UnitWeight']),str(val),str(quantity),str(from_server['Humidity']),str(from_server['Temperature'])))
           # print (conn.read())
            conn.close()

            #id, text = reader.read()
            #print(id)
            #print(text)

            #print (" The item with id " + id + " and name " + text + " has weight " + val)

            hx.power_down()
            hx.power_up()
            #client.close()

            time.sleep(1)


        except (KeyboardInterrupt, SystemExit):
             cleanAndExit()



finally:
        GPIO.cleanup()






#print (from_server)
