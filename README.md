## IoT-driven-Smart-Inventory-management-using-SCION-protocol-Integration-with-Alexa-AWS-and-Thingspeak

There are several Internet of things (IoT) applications running on legacy networks which are not flexible in terms of path selections, network outages and security concerns. Thus, the current situation demands switching over to a new network platform which is highly scalable, secure, and isolated in terms of its architecture. Thus, an IoT application is being attempted which will use <a href="https://www.scion-architecture.net">Scalable Control and Isolation on Next generation networks </a> (SCION) architecture and hence, surpasses the existing concerns on the current network protocols. The chosen Internet of things (IoT) application is based on Inventory Management wherein immediate actions like stock replenishment or availing discounts can be provided based on the monitored weights of the articles available for sale. The implementation follows a simple client server architecture in SCION wherein one autonomous system (AS) acts as the client and the other autonomous system (AS) acts as the server. The Autonomous systems are integrated with vivid range of cloud service providers like AWS and Thingspeak. We have also integrated our project with Alexa and AWS Lambda as an enhancement.

### BLOCK AND DEPLOYMENT DIAGRAM

<div align="center">
<Image src="Images/deployment.png" class="center" style="width:50%">
</div>

<div><h3>HARDWARE AND SOFTWARE SPECIFICATIONS</h3>
<ul>
  <li>Raspberry 3B+ <p>The application uses Raspberry Pi [2] as the micro-controller unit and around two Raspberry Pi [2] has been used upon which two separate SCION [1] AS nodes are installed respectively, one acts as the server interfaced with the RFID module and load [4] cell and the other acts as the client interfaced with the LCD unit where the weight data is being displayed (not within the scope of this report).</p></li>  
  
  <li>
  Load cell and Amplifier HX711 <p>As the main objective of application is to monitor and fetch the real time weight, load cell [4] of weight range up to 1 kg has been used. It is essentially a transducer that detects an applied load (force weight) and then changes it into an electrical signal output that is proportional to the load. The load causes a deformation in the dimensions of the underlying strain gauge; this deformation changes the electrical resistance which further changes the output electrical voltage as the wheat stone bridge is not balanced. The Load cell [4] consists of four pin outlets: red, black, green and white. 
  <br>
  
  The voltage signals which comes as output from the load cell [4] is then amplified with a HX711 [5] , a 24 bit analog to digital converter. This amplifier has got four pin outlets namely E+ (excitation) or VCC, E- (excitation) or ground and two outputs, that is A- and A+.
  
  </p>
  </li>
  
  <li>
  MFRC522 RFID reader <p>The MFRC522 [9] is a highly integrated reader/writer for contact-less communication. It uses the concept of radio-frequency identification and electromagnetic fields to transfer data over short distances. RFID employed in our project is useful to identify product data for further processing and analyzing. An RFID system uses RFID tags are attached to the object which is to be identified. Key chain and an electromagnetic card has been used in our project which has their own unique identification ids. It has got the following pins which are being utilized namely SDA, SCK, MOSI, MISO, GND, RST.</p>
  </li>
  
  <li>
  DHT11 sensor <p> A DHT11 sensor with operating voltage of 3.5-5.5v and current of 0.3A is opted for serial connection with Raspberry pi.</p>
  </li>
  
 <li>
  A mini 9v fan <p> A mini 9V fan is selected which is assumed to be the refrigeration coolant in our setup. It will be operated with wide range of methodologies like Alexa skill, manual operation via API server and temperature when it exceeds certain specified limit.</p>
  </li>
</ul>
</div>

### INTERFACING LOAD CELL, HX711 AMPLIFIER AND MFRC522 READER WITH PI

The HX711 [5] weight amplifier is interfaced with the load cell [4] using it’s following connections

• Excitation (E+) or VCC is red

• Excitation (E-) or ground is black

• Output (A+) is white

• Output (A-) is green

This load cell HX711 [5] integrated sensor unit is then interfaced with the Raspberry Pi serially as follows:

• Vcc of HX711 to Pin 2 (5V)

• GND to Pin 6 (GND)

• DT to Pin 29 (GPIO 5)

• SCK to Pin 31 (GPIO 6)

This sensor unit comprising of load cell [4] and HX711 [5] amplifier needs to be tested and calibrated accordingly to
ensure accurate weight readings after which real time weight data is acquired. Run the following command to **calibrate** the load cell after placing 2 objects of known weights.

                                            python3 example.py 
This file is present in HX711_Setup directory. Run this programm with some known weight product below 1 kg placed over load cell. Set the reference value obtained in the program.


RFID tags are attached to the product or pallet which is to be identified. The application primarily uses a card and a key
chain as the RFID tag. Each tag is associated with a unique id.The RFID reader sends a signal to the tag and read it’s
response. There are 8 hardware connections for RFID sensor with the Raspberry Pi [2] as follows:

• SDA connects to Pin 24

• SCK connects to Pin 23

• MOSI connects to Pin 19

• MISO connects to Pin 21

• GND connects to Pin 6

• RST connects to Pin 22

• 3.3v connects to Pin 1 

By default the Pi has the SPI (Serial Peripheral Interface) disabled, which is a prerequisite for the RFID reader
to function and therefore, needs to be enabled using rasp iconfig tool as follows:

• Run the command `sudo raspi-config`

• Select “Interfacing options”

• Select “P4 SPI” and then, select “Yes”

• Run the command “sudo reboot” to reboot the Pi

• Run the command `lsmod | grep spi` to check.

• And ensure if spi_bcm2835 is listed.



### COMMUNICATION FLOW

* Intially we need to set up a Mysql table to save up our product RFID data , type of the product and unit weight.Once these paramters are designed we run `productinput.py` in Register directory which would register the product.
* These registered products can be checked by querying the table directly in mysql or accessing the `retieve.php` page in PHP show products directory which basically runs a select query and outputs the contents of the product table.

<Image src="Images/PHP_Products.PNG" class="center" style="width:50%">

* Once the registration process is done,we tend to integrate RFID part, Temperature/Humidity and Load cell part.
* The DHT11 sensor is connected to Raspberry pi serially via Breadboard to obtain Humdity/Temperature of the area where we implment our setup.
* The intgeration is done by running 2 independent python programs and coupling it using socket server networking with unique ip and ports employed.One python program acts as the server and outputs Temprature/Humidty readings and Unit weight of the products based on the RFID placed. To start this program run 
        `python3 mainsocketserverre.py` 
 which can be found in RFID_DHT11_Socket_Server directory.
 * Once this values are obtained into the client part using the python socket networking protocol, it is coupled with the weight readings obtained by the Load cell.This is the most signifcant program in this setup since there are multiple functionalites coupled with it.
 * The client program after obtaining RFID/Tempertaure/Humidity/UnitWeight calculates
              o Calculates the weight of the product based on the values obtained from Load cell.
              o Calcualtes the overall weight and the no of quanity based on total weight and unit weight.
              o Publishes all obtained values to remote system running Node-RED (to visualize) via MQTT protocol over SCION sig                         configuration.
              o Scion Sig can be installed using the [link](https://code.ovgu.de/hausheer/scion-iot/tree/UPS_Failover/UPS_Failover/setup_sig) and Mosquitto [broker](https://appcodelabs.com/introduction-to-iot-build-an-mqtt-server-using-raspberry-pi) for MQTT can be installed using the link.
              o Pubishes these data to the Cloud service Thinkspeak channel that we configure.
              o Auto updates the AWS shadow by turning on the refrigeration fan, whenever the temperature detected is greater than a                     specified threshold ( in our case 22 degree celsius).
              
This program is run by running
           `python3 cloud_socket.py`
which can be found in RFID_Weight_MQTT_Client_Cloud directory.
* Next we configure and setup Thinkspead channel for our data to be visualized. Please refer the [link](https://de.mathworks.com/help/thingspeak/collect-data-in-a-new-channel.html) to configure a channel and alter the specifications as per the paramters.
* Then we need to setup an account with Amazon AWS. Once done we need to open AWS IoT core and register a thing to proceed. A thing is bascially a virtual representation of our device (Refrigeration fan in our case). Please refer the [link](https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html) to set up a thing and integrte with our setup.

<Image src="Images/AWS_Shadow_Example.PNG" class="center" style="width:50%">
  <Image src="Images/AWS_ESP_thing.PNG" class="center" style="width:50%">
  
* Once AWS thing is setup we tend to update its Shadow state each time whenever we turn on/off the fan.We also configure AWS simple notifcation service to act and notify the end users/warehouse representatives by sending a mail and SMS whenever the refrigeration fan is turned on. Refer the [link](https://docs.aws.amazon.com/iot/latest/developerguide/iot-sns-rule.html) to setup SNS and the [link](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html) to get an idea on AWS shadow and its significance.

<Image src="Images/AWS_notification_fan_on.PNG" class="center" style="width:50%">
 
<Image src="Images/AWS_Mail_Notification.PNG" class="center" style="width:50%"> 

* Then we run a code `python3 ledcontroller.py` to control the refrigeration fan connected to pi and based on the AWS thing shadow values obatined.
* As of now the fan would only switch on once the temperature exceeds a certain limit. We have incorporated addtional enhancements where this refrigeration fan can be manully turned. Some of the methods are

o A Python FLask api server is hosted in Raspberry pi which allows users to turn off/turn off the fan using the web interface.
o The users have the provision to turnon/turnoff the fan with an Alexa skill controlled over voice command.We have also integrated this   alexa skill with Thingspeak cloud so that the user could fetch our the product/weather details with his/her voice commands.

<Image src="Images/AWS_Mail_Notification.PNG" class="center" style="width:50%"> 

#### Flask API server

Please make sure that Flask framework is installed in Raspberry pi. Run the command `flaskserver.py` in the FanControllerSwitch directory to start the Flask api server and control the Refrigeration fan using the web interface. The fan can be simply be controlled with Command prompt code `newledswitch.py` in CommandPrompt directory in FanControllerSwitch.

<Image src="Images/Flask_WebUI_Switch.PNG" class="center" style="width:50%"> 


#### Alexa Skill Kit

We tend to integrate ALexa skill with our system. Hence we created a Alexa skill that communicates with Alexa Lambda (serverless computing platform) which in turn communicates with AWS IoT Core to update shadow and turn on/off the refrigeration fan. The skill as discussed is also integrated with another cloud service Thingspeak to fetch out the product details. Hence the end user would be able to get product details like weight/unitweight/type/name/quanitity/temperature and humidity of warehouse and also provisions to turn on/off the refrigeration fan. Make sure the user has enabled the link in his/her alexa skill app. Please refer the [link](http://developer.amazon.com/alexa/console/ask) to get an understanding of Alexa SKill kit and [link](https://docs.aws.amazon.com/lambda/latest/dg/services-alexa.html) to gain understaning on AWS lambda. The code in the directories Alexa_HomeIoT_skill and Alexa_Lambda_Node.js can be used for reference.


**Note : Turning off the refrigeration fan has been configured as a manual process considering the saftey factor.Once the temperature is back to normal, we expect warehouse authorities to manually turn off the process. This is the reason why this operation was not automated.**

### OUTPUT


##### <ins> Product Details Visualization </ins>
As discussed the Output (product details) can be obatined via Thingspeak channel and Node-Red ui. Audio output is obtained via Amazon echo using alexa skill kit.

Make sure [NodeRed](https://nodered.org/docs/getting-started/raspberrypi) is installed in a remote system and connected to the Mosquitto broker in the pi via its MQTT node. This remote MQTT connection in our project has been set up with the help of SCION sig gatway protocol. Please refer the link to install sig gatway. It helps in establishing MQTT connections between 2 remote systems.The data obtained in Node-Red is visualized using Node-Red ui.


<Image src="Images/Node-Red_UI.PNG" class="center" style="width:50%"> 

Similarly the data obtained in Thinkspead cloud is visualized using different plots in its respective channel. With Thingspeak we have the provisions to incorporate **Matlab features** and processing into the data obtained in the channel. Using the Temp/Humidity obtained in our channel we have calculated Dew point based on Matlab processing and visualized in another channel. 

<Image src="Images/Productdata1.PNG" class="center" style="width:50%"> 
  
  <Image src="Images/Productdata2.PNG" class="center" style="width:50%"> 
  
   <Image src="Images/DewPoint.PNG" class="center" style="width:50%"> 

##### <ins> Fan Operation </ins>

As discussed the refrigeration fan will be operated in case of Tempertaure rise , API server and Alexa audio command.

##### <ins> Alexa Audio output </ins>

Alexa resonates the response status and product data based on the question asked and the output obatined from the Thingspeak/AWS cloud



