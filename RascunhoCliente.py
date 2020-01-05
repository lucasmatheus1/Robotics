#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from ev3dev.ev3 import *

ultra = 0.0
MOTOR = LargeMotor("outA")

client = mqtt.Client()
client.connect("169.254.74.170", 1883, 60)

def on_connect(client, userdata, flags, rc):
    client.subscribe([("topic/teste", 0)])

def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

def on_message(client, userdata, msg):
    global ultra

    if msg.topic == "topic/teste":
        ultra = float(msg.payload)

def andar():
    global ultra

    if ultra < 30.0:
        MOTOR.run_forever(speed_sp = 200)

    print (ultra)

def main():

        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_start()

        while True:
            andar()

if __name__ == '__main__':
    main()
