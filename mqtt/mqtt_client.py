import time
from machine import I2C
from machine import Pin,Timer
from sht25 import SHT25
from umqtt.simple import MQTTClient

sensor = SHT25(I2C(scl=Pin(1), sda=Pin(3)))
led=Pin(16,Pin.OUT)

def do_pub(c):
    temperature = sensor.getTemperature()
    humidity = sensor.getHumidity()
    message = str(temperature) + '|' + str(humidity)
    c.publish(b"pyespcar_basic_control", message)

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"on":
        led.value(0)
        state = 1
    elif msg == b"off":
        led.value(1)
        state = 0
    elif msg == b"toggle":
        led.value(state)
        state = 1 - state

c = MQTTClient("umqtt_client", '192.168.31.11')
c.set_callback(sub_cb)
c.connect()
c.subscribe(b"led_toggle")

tim = Timer(-1)
tim.init(period=60000, mode=Timer.PERIODIC, callback=lambda t:do_pub(c))

while True:
	c.wait_msg()
c.disconnect()
