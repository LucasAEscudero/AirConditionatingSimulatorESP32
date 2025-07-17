import time
import machine
import micropython
import network
from machine import Pin, ADC, PWM
from umqtt.simple import MQTTClient
import math
import time

# wifi connection
ssid = 'Wokwi-GUEST'
wifiPassword = ''
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, wifiPassword)
print('Connected')
while not sta_if.isconnected():
    print('.', end="")
    time.sleep(0.1)
print('Connected at Wifi!')
print(sta_if.ifconfig()) # print IP

# Adafruit Broker (MQTT) connection
mqtt_server = 'io.adafruit.com'
port = 1883
user = 'lucasescud'
password = os.getenv("ADAFRUIT_IO_KEY") or ''
client_id = 'air_cond_sim_id'
topic_NTCSensor = 'lucasescud/feeds/NTCSensor'
topic_TempUmbral = 'lucasescud/feeds/TempUmbral'
topic_TempUmbralControl = 'lucasescud/feeds/TempUmbralControl'

def createTempMessage(temp):
    return (str(temp) + "°C").encode('utf-8')

def mqttCallback(topic, msg):
    dato = msg.decode('utf-8')
    topicrec = topic.decode('utf-8')
    # print("Message in topic " + topicrec + ": " + dato)
    if topicrec == topic_TempUmbralControl and int(dato):
        global umbralTemp, newUmbral
        umbralTemp = umbralTemp + int(dato) # 0, 1 or -1
        newUmbral = True
        connectionMQTT.publish(topic_TempUmbral, createTempMessage(umbralTemp))
        

try:
    connectionMQTT = MQTTClient(client_id, mqtt_server, user=user, password=password, port=int(port))
    connectionMQTT.set_callback(mqttCallback)
    connectionMQTT.connect()
    connectionMQTT.subscribe(topic_TempUmbralControl)
    print("Conectado con Broker MQTT")
except OSError as err:
    print("Fallo la conexión al Broker, reiniciando...")
    time.sleep(5)
    machine.reset()

# config NTC sensor
BETA = 3950
R_FIXED = 10000
T0 = 298.15
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)

# set init values and get pins
umbralTemp = 24
newUmbral = False
connectionMQTT.publish(topic_TempUmbral, createTempMessage(umbralTemp))

previousTemp = 0
coldPreviousState = False
coldPin = PWM(Pin(23, Pin.OUT))
coldPin.freq(50)
coldPin.duty(25) # set in ang 0
nothingPin = Pin(16, Pin.OUT)
hotPin = Pin(2, Pin.OUT)

def readNtcTemp():
    raw = adc.read_u16()
    tempCalc = 1 / (math.log(1 / (65535 / raw - 1)) / BETA + 1.0 / T0) - 273.15
    return round(tempCalc)

def changeCondStatus(cold, nothing, hot):
    nothingPin.value(nothing)
    hotPin.value(hot)

    global coldPreviousState
    if cold != coldPreviousState:
        coldPreviousState = cold
        coldPin.duty(75 if cold else 25)

while True:
    try:
        temp = readNtcTemp()
        # print(f"Temperatura: {temp} °C")

        if previousTemp != temp or newUmbral:
            newUmbral = False
            previousTemp = temp
            connectionMQTT.publish(topic_NTCSensor, createTempMessage(temp))

            if temp == umbralTemp:
                changeCondStatus(0, 1, 0)
            elif temp > umbralTemp:
                changeCondStatus(1, 0, 0)
            else:
                changeCondStatus(0, 0, 1)

        connectionMQTT.check_msg()

        time.sleep(1)
    except OSError as err:
        print("Error: ", err)
        time.sleep(5)
        machine.reset()
    
