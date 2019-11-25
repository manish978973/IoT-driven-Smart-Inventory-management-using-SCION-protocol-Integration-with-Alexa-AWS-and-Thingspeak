import paho.mqtt.client as mqtt
import ssl, time, sys


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

mqttc = mqtt.Client("client1")

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


print ("Enter 1 to Turn On the LED")
print ("Enter 2 to Turn OFF the LED")
print ("Enter 3 to exit")


while True: 
   data = input("Select an option:")
   if data == "1":
	   mqttc.publish(SHADOW_UPDATE_TOPIC,SHADOW_STATE_DOC_LED_ON,qos=1)
   elif data == "2":
	   mqttc.publish(SHADOW_UPDATE_TOPIC,SHADOW_STATE_DOC_LED_OFF,qos=1)
   elif data == "3":
	   sys.exit() 
   else:
	   print("Invalid input try again...")
	   sys.exit() 


