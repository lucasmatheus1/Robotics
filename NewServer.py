#!/usr/bin/env python3

from ev3dev.ev3 import *
import paho.mqtt.client as mqtt
from os import system
from time import sleep


def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

def connect(client):
    client.connect("localhost", 1883, 60)
    client.on_disconnect = on_disconnect

def send(client, ultrassonico, distanciaPermitida, botao):
    while True:
        ultrassonicoAtual = ultrassonico.value() / 10

        # if botao.enter:
        #     print("\n\n\n\n\n\n\n\n\n\n   ----- Iniciou novamente -----")
        #     system("clear")

        if ultrassonicoAtual <= distanciaPermitida:
            client.publish(topic="topic/sensor/ultra", payload=True, qos=0, retain=False)
            print(ultrassonicoAtual)
            ultrassonicoAtual = 100000
            sleep(1)
            system("clear")
            break

    connect(client)
    send(client, ultrassonico, distanciaPermitida, botao)


ultrassonico = UltrasonicSensor('in1')
client = mqtt.Client()

distanciaPermitida = 20
botao = Button()

connect(client)
send(client, ultrassonico, distanciaPermitida, botao)

# print("\n\n\n\n\n\n\n\n\n\n   ----- Botao do meio para iniciar -----")
# while True:
#     if botao.enter:
#         system("clear")
#         break
