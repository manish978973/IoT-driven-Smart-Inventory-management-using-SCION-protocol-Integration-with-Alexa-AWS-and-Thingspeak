import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import ssl, time, sys, json


MQTT_HOST = "afio7p37diyt8-ats.iot.eu-west-1.amazonaws.com"
CA_ROOT_CERT_FILE = "/home/pi/AmazonRootCA1.pem"
THING_NAME = "ESP"
THING_CERT_FILE = "/home/pi/f88bbe537b-certificate.pem.crt"
THING_PRIVATE_KEY_FILE = "/home/pi/f88bbe537b-private.pem.key"

LED_PIN = 21
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
SHADOW_UPDATE_TOPIC = "$aws/things/" + THING_NAME + "/shadow/update"
SHADOW_UPDATE_ACCEPTED_TOPIC = "$aws/things/" + THING_NAME + "/shadow/update/accepted"
SHADOW_UPDATE_REJECTED_TOPIC = "$aws/things/" + THING_NAME + "/shadow/update/rejected"
SHADOW_UPDATE_DELTA_TOPIC = "$aws/things/" + THING_NAME + "/shadow/update/delta"
SHADOW_GET_TOPIC = "$aws/things/" + THING_NAME + "/shadow/get"
SHADOW_GET_ACCEPTED_TOPIC = "$aws/things/" + THING_NAME + "/shadow/get/accepted"
SHADOW_GET_REJECTED_TOPIC = "$aws/things/" + THING_NAME + "/shadow/get/rejected"
SHADOW_STATE_DOC_LED_ON = """{"state" : {"reported" : {"LED" : "ON"}}}"""
SHADOW_STATE_DOC_LED_OFF = """{"state" : {"reported" : {"LED" : "OFF"}}}"""



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

mqttc = mqtt.Client("client2")


def LED_Status_Change(Shadow_State_Doc, Type):
	# Parse LED Status from Shadow
	DESIRED_LED_STATUS = ""
	print ("\nParsing Shadow Json...")
	SHADOW_State_Doc = json.loads(Shadow_State_Doc)
	if Type == "DELTA":
		DESIRED_LED_STATUS = SHADOW_State_Doc['state']['LED']
	elif Type == "GET_REQ":
		DESIRED_LED_STATUS = SHADOW_State_Doc['state']['desired']['LED']
	print ("Desired LED Status: " + DESIRED_LED_STATUS)

	# Control LED
	if DESIRED_LED_STATUS == "ON":
		# Turn LED ON
		print ("\nTurning ON LED...")
		GPIO.output(LED_PIN, GPIO.HIGH)
		# Report LED ON Status back to Shadow
		print ("LED Turned ON. Reporting ON Status to Shadow...")
		mqttc.publish(SHADOW_UPDATE_TOPIC,SHADOW_STATE_DOC_LED_ON,qos=1)
	elif DESIRED_LED_STATUS == "OFF":
		# Turn LED OFF
		print ("\nTurning OFF LED...")
		GPIO.output(LED_PIN, GPIO.LOW)
		# Report LED OFF Status back to Shadow
		print ("LED Turned OFF. Reporting OFF Status to Shadow...")
		mqttc.publish(SHADOW_UPDATE_TOPIC,SHADOW_STATE_DOC_LED_OFF,qos=1)
	else:
		print ("---ERROR--- Invalid LED STATUS.")


def on_connect(mqttc, obj,flags, rc):
	print ("Connected to AWS IoT...")
	# Subscribe to Delta Topic
	mqttc.subscribe(SHADOW_UPDATE_DELTA_TOPIC, 1)
	# Subscribe to Update Topic
	#mqttc.subscribe(SHADOW_UPDATE_TOPIC, 1)
	# Subscribe to Update Accepted and Rejected Topics
	mqttc.subscribe(SHADOW_UPDATE_ACCEPTED_TOPIC, 1)
	mqttc.subscribe(SHADOW_UPDATE_REJECTED_TOPIC, 1)
	# Subscribe to Get Accepted and Rejected Topics
	mqttc.subscribe(SHADOW_GET_ACCEPTED_TOPIC, 1)
	mqttc.subscribe(SHADOW_GET_REJECTED_TOPIC, 1)






def on_message(mqttc, obj, msg):
	if str(msg.topic) == SHADOW_UPDATE_DELTA_TOPIC:
		print ("\nNew Delta Message Received...")
		SHADOW_STATE_DELTA = str(msg.payload.decode())
		print (SHADOW_STATE_DELTA)
		LED_Status_Change(SHADOW_STATE_DELTA, "DELTA")
	elif str(msg.topic) == SHADOW_GET_ACCEPTED_TOPIC:
		print ("\nReceived State Doc with Get Request...")
		SHADOW_STATE_DOC = str(msg.payload.decode())
		print (SHADOW_STATE_DOC)
		LED_Status_Change(SHADOW_STATE_DOC, "GET_REQ")
	elif str(msg.topic) == SHADOW_GET_REJECTED_TOPIC:
		SHADOW_GET_ERROR = str(msg.payload.decode())
		print ("\n---ERROR--- Unable to fetch Shadow Doc...\nError Response: " + SHADOW_GET_ERROR)
	elif str(msg.topic) == SHADOW_UPDATE_ACCEPTED_TOPIC:
		print ("\nLED Status Change Updated SUCCESSFULLY in Shadow...")
		print ("Response JSON: " + str(msg.payload.decode()))
	elif str(msg.topic) == SHADOW_UPDATE_REJECTED_TOPIC:
		SHADOW_UPDATE_ERROR = str(msg.payload.decode())
		print ("\n---ERROR--- Failed to Update the Shadow...\nError Response: " + SHADOW_UPDATE_ERROR)
	else:
		print ("AWS Response Topic: " + str(msg.topic))
		print ("QoS: " + str(msg.qos))
		print ("Payload: " + str(msg.payload.decode()))




def on_subscribe(mqttc, obj, mid, granted_qos):
	#As we are subscribing to 3 Topics, wait till all 3 topics get subscribed
	#for each subscription mid will get incremented by 1 (starting with 1)
	if mid == 3:
		# Fetch current Shadow status. Useful for reconnection scenario.
		mqttc.publish(SHADOW_GET_TOPIC,"",qos=1)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print ("Diconnected from AWS IoT. Trying to auto-reconnect...")



mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect


mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY_FILE, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

# Continue monitoring the incoming messages for subscribed topic
mqttc.loop_forever()
