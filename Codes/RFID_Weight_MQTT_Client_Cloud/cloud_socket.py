#! /usr/bin/python3
import RPi.GPIO as GPIO
import socket
import json
import time
import sys
import paho.mqtt.client as paho
import urllib.request
import ssl





#amazon AWS details
MQTT_HOST = "afio7p37diyt8-ats.iot.eu-west-1.amazonaws.com"
CA_ROOT_CERT_FILE = "/home/pi/AmazonRootCA1.pem"
THING_NAME = "ESP"
THING_CERT_FILE = "/home/pi/f88bbe537b-certificate.pem.crt"
THING_PRIVATE_KEY_FILE = "/home/pi/f88bbe537b-private.pem.key"


MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
SHADOW_UPDATE_TOPIC = "$aws/things/" + THING_NAME + "/shadow/update"
SHADOW_UPDATE_ACCEPTED_TOPIC = "$aws/things/" + THING_NAME + "/shadow/update/accepted"
SHADOW_UPDATE_REJECTED_TOPIC = "$aws/things/" + THING_NAME + "/shadow/update/rejected"
SHADOW_STATE_DOC_LED_ON = """{"state" : {"desired" : {"LED" : "ON"}}}"""
SHADOW_STATE_DOC_LED_OFF = """{"state" : {"desired" : {"LED" : "OFF"}}}"""
SHADOW_GET_TOPIC = "$aws/things/" + THING_NAME + "/shadow/get"
SHADOW_GET_ACCEPTED_TOPIC = "$aws/things/" + THING_NAME + "/shadow/get/accepted"
SHADOW_GET_REJECTED_TOPIC = "$aws/things/" + THING_NAME + "/shadow/get/rejected"


mqttc = paho.Client("client1")

def on_connect(mqttc, obj,flags, rc):
        mqttc.subscribe(SHADOW_UPDATE_ACCEPTED_TOPIC, 1)
        mqttc.subscribe(SHADOW_UPDATE_REJECTED_TOPIC, 1)


def on_message(mqttc, obj, msg):
    if str(msg.topic) == SHADOW_UPDATE_ACCEPTED_TOPIC:
        print ("\n---SUCCESS---\nShadow State Doc Accepted by AWS IoT.")
        print ("Response JSON:\n" + str(msg.payload.decode()))
    elif str(msg.topic) == SHADOW_UPDATE_REJECTED_TOPIC:
        print ("\n---FAILED---\nShadow State Doc Rejected by AWS IoT.")
        print ("Error Response JSON:\n" + str(msg.payload.decode()))



def on_subscribe(mqttc, obj, mid, granted_qos):
    if mid == 3:
            # Fetch current Shadow status. Useful for reconnection scenario.
            mqttc.publish(SHADOW_GET_TOPIC,"",qos=1)


mqttc.on_connect = on_connect

mqttc.on_message = on_message
#mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe


mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY_FILE, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.loop_start()













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
            if (from_server['Temperature'] > 22):
                mqttc.publish(SHADOW_UPDATE_TOPIC,SHADOW_STATE_DOC_LED_ON,qos=1)
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
