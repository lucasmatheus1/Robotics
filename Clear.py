#!/usr/bin/env python3
from time import sleep
from ev3dev.ev3 import *
import paho.mqtt.client as mqtt
from Resgate import *
from os import system


def girar_90D():
    for i in range(450):
        motorDireito.run_forever(speed_sp=-200)
        motorEsquerdo.run_forever(speed_sp=200)
    motorEsquerdo.stop()
    motorDireito.stop()


def girar_90E():
    for i in range(450):
        motorDireito.run_forever(speed_sp=200)
        motorEsquerdo.run_forever(speed_sp=-200)
    motorEsquerdo.stop()
    motorDireito.stop()


def girar_180():
    for i in range(820):
        motorDireito.run_forever(speed_sp=200)
        motorEsquerdo.run_forever(speed_sp=-200)
    motorEsquerdo.stop()
    motorDireito.stop()


def funcao_saturacao(v):
    if v > 1000:
        return 1000
    elif v < -1000:
        return -1000
    else:
        return v


def sair_Quadrado():
    global ultra

    print("Funcao sair do quadrado")

    cont = 0

    while sensorCorEsquerdo.value() != preto:
        motorEsquerdo.run_forever(speed_sp=225)
        motorDireito.run_forever(speed_sp=200)

    motorEsquerdo.stop()
    motorDireito.stop()
    deixar_boneco()

    while cont <= 4:
        if cont == 0 or cont == 2 or cont == 4:
            girar_90D()

        else:
            for i in range(1500):
                motorEsquerdo.run_forever(speed_sp=300)
                motorDireito.run_forever(speed_sp=300)
            for i in range(50):
                motorEsquerdo.run_forever(speed_sp=-200)
                motorDireito.run_forever(speed_sp=-200)

        cont += 1

    while True:
        if sensorCorEsquerdo.value() == verde:
            while sensorCorDireito.value() != verde:
                motorDireito.run_forever(speed_sp=100)
                motorEsquerdo.run_forever(speed_sp=30)
                if sensorCorDireito.value() == verde:
                    break
            while sensorCorDireito.value() != vermelho:
                motorDireito.run_forever(speed_sp=100)
                motorEsquerdo.run_forever(speed_sp=30)

            while sensorCorDireito.value() != azul:
                motorDireito.run_forever(speed_sp=100)

            seguirFrente(azul)
            break

        else:
            PID_SairQuadrado()

    motorEsquerdo.stop()
    motorDireito.stop()
    ultra = False


def deixar_boneco():

    for i in range(500):
        motorEsquerdo.run_forever(speed_sp=200)
        motorDireito.run_forever(speed_sp=200)
    motorEsquerdo.stop()
    motorDireito.stop()

    for i in range(10):
        motorPorta.run_forever(speed_sp=-1000)

    for i in range(250):
        motorEsquerdo.run_forever(speed_sp=-200)
        motorDireito.run_forever(speed_sp=-200)

    sleep(1)

    for i in range(10):
        motorPorta.run_forever(speed_sp=+1000)

    motorEsquerdo.stop()
    motorDireito.stop()

    resgate.temBoneco = False


def pegar_Boneco():
    global ultra
    print("Pegar boneco")

    motorPorta.stop()
    cont = 0

    while cont <= 5:

        if cont == 0:
            for i in range(10):
                motorPorta.run_forever(speed_sp=-1000)

        elif cont == 1:
            girar_90D()
            sleep(1)

        elif cont == 2:
            for i in range(300):
                motorEsquerdo.run_forever(speed_sp=200)
                motorDireito.run_forever(speed_sp=200)

            sleep(1)

        elif cont == 3:
            for i in range(10):
                motorPorta.run_forever(speed_sp=+1000)

        elif cont == 4:
            for i in range(300):
                motorEsquerdo.run_forever(speed_sp=-200)
                motorDireito.run_forever(speed_sp=-200)
            sleep(1)

        else:
            girar_90E()

        cont += 1

    for i in range(100):
        motorDireito.run_forever(speed_sp=300)
        motorEsquerdo.run_forever(speed_sp=300)


    motorEsquerdo.stop()
    motorDireito.stop()

    resgate.temBoneco = True
    ultra = False


def PID_SairQuadrado():
    offset = 8
    constProp = 30

    erro = offset - sensorInfraEsquerdo.value()
    giro = erro * constProp

    if erro > 8:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(100 + giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(1250 - giro))
    elif erro < 8:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(200 + giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(200 - giro))


def FINALMENTE():
    offset = 28

    constProp = 50
    erro = offset - sensorInfraEsquerdo.value()

    giro = constProp * erro

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(500 - giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(500 + giro))


def andarSensorEsquerdo():
    global  temporizador,  indo_voltando, contCores, ultra

    # if botao.enter:
    #     print("\n\n\n\n\n\n\n\n\n\n   ----- Iniciar novamente -----")
    #     system("clear")
    #     temBoneco = False
    #     ultra = False
    #     indo_voltando = True
    #     contCores = 0
    #
    # if botao.down:
    #     print("\n\n\n\n\n\n\n\n\n\n   ----- Iniciar novamente do zero -----")
    #     motorEsquerdo.stop()
    #     motorDireito.stop()
    #     motorPorta.stop()
    #     main()

    offset = 28
    constProp = 40
    erro = offset - sensorInfraEsquerdo.value()

    giro = constProp * erro

    if ultra and not resgate.temBoneco:
        print("PEGAR BONECO")
        motorEsquerdo.stop()
        motorDireito.stop()
        pegar_Boneco()

    cor = sensorCorDireito.value()
    if (cor == azul) or (cor == verde) or (cor == vermelho):
        temporizador = True

    if (sensorCorDireito.value() == branco) and (sensorInfraEsquerdo.value() < 22):
        if not temporizador:
            print("PLATAFORMA")
            andarSensorDireito()
        else:
            for i in range(150):
                FINALMENTE()
            temporizador = False

    else:
        motorEsquerdo.run_forever(speed_sp=funcao_saturacao(500 - giro))
        motorDireito.run_forever(speed_sp=funcao_saturacao(500 + giro))


def andarSensorDireito():
    global temporizador

    offset = 29
    constProp = 50

    erro = offset - sensorInfraDireito.value()
    giro = erro * constProp

    # if ultra and not resgate.temBoneco:
    #     motorEsquerdo.stop()
    #     motorDireito.stop()
    #     pegar_Boneco()

    motorEsquerdo.run_forever(speed_sp=funcao_saturacao(500 + giro))
    motorDireito.run_forever(speed_sp=funcao_saturacao(500 - giro))


def virarDireita():
    print("===== VIRAR DIREITA =====")
    for i in range(450):
        andarSensorDireito()


def virarEsquerda():
    print("===== VIRAR ESQUERDA =====")
    for i in range(200):
        andarSensorEsquerdo()


def alinhar(cor):

    while sensorCorEsquerdo.value() == cor or sensorCorDireito.value() == cor:

        if sensorCorDireito.value() != branco:
            motorDireito.run_forever(speed_sp=-80)
            motorEsquerdo.run_forever(speed_sp=30)

        if sensorCorEsquerdo.value() != branco:
            motorEsquerdo.run_forever(speed_sp=-80)
            motorDireito.run_forever(speed_sp=30)


def seguirFrente(cor):
    print("===== SEGUIR EM FRENTE =====")

    alinhar(cor)
    for i in range(1070):
        motorEsquerdo.run_forever(speed_sp=200)
        motorDireito.run_forever(speed_sp=200)


def saberGiro(cont):
    if cont == 1:
        return "Esquerda"
    elif cont == 2:
        return "Seguir"
    elif cont >= 3:
        return "Direita"


def moda(l):
    repeticoes = 0
    valor = 0
    for i in range(len(l)):
        aparicoes = l.count(l[i])
        if aparicoes > repeticoes:
            repeticoes = aparicoes
            valor = l[i]

    return valor


def verificarCor():

    listaDeCor = []

    for i in range(20):
        motorEsquerdo.run_forever(speed_sp=100)
        motorDireito.run_forever(speed_sp=100)
        listaDeCor.append(sensorCorEsquerdo.value())

    return moda(listaDeCor)


def SaberLado(cor):
    print(" ======== APRENDENDO A COR ========")

    contCor = 0
    contCorTotal = 0

    coresIndesejadas = [7, 6, 1, 0, 4]

    ultimaCOR = 0

    while True:
        andarSensorEsquerdo()

        if ultimaCOR == sensorCorEsquerdo.value() and sensorCorEsquerdo.value() != preto:
            if verificarCor() == ultimaCOR:
                return saberGiro(contCorTotal)

        if (sensorCorEsquerdo.value() != cor and sensorCorEsquerdo.value() not in coresIndesejadas) or contCorTotal >= 3:
            if verificarCor() == sensorCorEsquerdo.value():
                return saberGiro(contCorTotal)

        while sensorCorEsquerdo.value() == cor:
            andarSensorEsquerdo()
            contCor += 1
            ultimaCOR = cor

        if contCor > 1:
            contCorTotal += 1
            contCor = 0

        while sensorCorEsquerdo.value() == preto or sensorCorEsquerdo.value() == semCor:
            andarSensorEsquerdo()
            ultimaCOR = preto


def mudarSentidos(cor):
    if cor == "Seguir":
        return "Seguir"
    elif cor == "Esquerda":
        return "Direita"
    else:
        return "Esquerda"


def Acao(acao, cor):
    if acao == "Seguir":
        seguirFrente(cor)
    elif acao == "Direita":
        virarDireita()
    elif acao == "Esquerda":
        virarEsquerda()


def on_connect(client, userdata, flags, rc):
    client.subscribe([("topic/sensor/ultra", 0)])


def on_disconnect(client, userdata, rc=0):
    client.loop_stop()


def on_message(client, userdata, msg):
    global ultra

    if msg.topic == "topic/sensor/ultra":
        ultra = bool(msg.payload)
    print(" kjasbdliarfgbaoiwyrgfowieufbaoiufbapufbaoruifawoifu",ultra)

def main():

    global ultra, indo_voltando, contCores
    corVermelha = ""
    corVerde = ""
    corAzul = ""

    try:

        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_start()

        # print("\n\n\n\n   ----- Botao do meio para iniciar -----")
        # while True:
        #
        #     if botao.enter:
        #         system("clear")
        #         temBoneco = False
        #         ultra = False
        #         break

        while True:

            print("VOLTS: ", power.measured_volts)
            print("Cor verde: ", corVerde)
            print("Cor vermelha: ", corVermelha)
            print("Cor azul: ", corAzul)
            print("Quantidades de cores: ", contCores)
            print("Tem boneco? ", resgate.temBoneco)
            print("Ultra: ", ultra)
            print("COR Esquerdo: ", sensorCorEsquerdo.value())
            print("COR Direito", sensorCorDireito.value())

            if indo_voltando:

                if (contCores >= 6) and (sensorCorEsquerdo.value() == azul) and (not resgate.temBoneco):
                    print("NAO TEM BONECO <=> VOLTANDO")

                    girar_180()

                    indo_voltando = False
                    corAzul = mudarSentidos(corAzul)
                    corVermelha = mudarSentidos(corVermelha)
                    corVerde = mudarSentidos(corVerde)
                    contCores = 0

                if (contCores >= 6) and (sensorCorEsquerdo.value() == azul) and resgate.temBoneco:
                    print("ENTRANDO NO QUADRADO COM O BONECO")
                    seguirFrente(azul)
                    sair_Quadrado()
                    indo_voltando = False
                    corAzul = mudarSentidos(corAzul)
                    corVermelha = mudarSentidos(corVermelha)
                    corVerde = mudarSentidos(corVerde)
                    contCores = 0
            else:
                if contCores >= 6:
                    girar_180()

                    indo_voltando = True
                    corAzul = mudarSentidos(corAzul)
                    corVermelha = mudarSentidos(corVermelha)
                    corVerde = mudarSentidos(corVerde)
                    contCores = 0



            if (sensorCorEsquerdo.value() == branco) or (sensorCorEsquerdo.value() == preto):
                andarSensorEsquerdo()
                print()

            elif sensorCorEsquerdo.value() == azul:
                contCores += 1
                if corAzul == "":
                    corAzul = SaberLado(azul)

                else:
                    Acao(corAzul, azul)

            elif sensorCorEsquerdo.value() == verde:
                contCores += 1
                if corVerde == "":
                    corVerde = SaberLado(verde)

                else:
                    Acao(corVerde, verde)

            elif sensorCorEsquerdo.value() == vermelho:
                contCores += 1
                if corVermelha == "":
                    corVermelha = SaberLado(vermelho)

                else:
                    Acao(corVermelha, vermelho)

    except KeyboardInterrupt:
        motorEsquerdo.stop()
        motorDireito.stop()
        motorPorta.stop()


resgate = Resgate()
client = mqtt.Client()
client.connect("169.254.61.245", 1883, 60)

motorEsquerdo = LargeMotor('outB')
motorDireito = LargeMotor('outC')


motorPorta = LargeMotor('outD')

sensorInfraEsquerdo = InfraredSensor("in1")
sensorInfraDireito = InfraredSensor("in2")

sensorCorEsquerdo = ColorSensor("in3")
sensorCorDireito = ColorSensor("in4")
sensorCorEsquerdo.mode = 'COL-COLOR'
sensorCorDireito.mode = 'COL-COLOR'

botao = Button()
power = PowerSupply()

semCor, preto, azul, verde, vermelho, branco = 0, 1, 2, 3, 5, 6

contCores = 0
indo_voltando = True
temporizador = False
ultra = False

print("---------------------")
print("------ INICIOU ------")
print("---------------------")

if __name__ == '__main__':
    main()
