#### IoT-driven-Smart-Inventory-management-using-SCION-protocol-Integration-with-Alexa-AWS-and-Thingspeak

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
  DHT11 sensor <p> A DHT11 sensor with operating voltage of 3.5-5.5v and current of 0.3A is opted for serial connection with Rasoberry pi.</p>
  </li>
  
    <li>
  A mini 9v fan <p> A mini 9V fan is selected which is assumed to be the refrigeration coolant in our setup. It will be operated with wide range of methodologies like Alexa skill, manual operation via API server and temperature when it exceeds certain specified limit.</p>
  </li>
</ul>
</div>
