def pegar_Boneco():
    motorPorta.run_forever(speed_sp=100)
    cont = 0
    while cont <= 4:
        posicao_motor_D = motorDireito.position
        posicao_motor_E = motorEsquerdo.position
        if cont == 0 or cont == 4:
            qtd = 700
        elif cont == 1 or cont == 3:
            qtd = 300
        else:
            qtd = 300

        for i in range(qtd):
            if cont == 0:
                motorDireito.run_to_abs_pos(position_sp=posicao_motor_D + 600, speed_sp=100)
                motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E - 600, speed_sp=100)
            elif cont == 1:
                motorEsquerdo.run_forever(speed_sp=300)
                motorDireito.run_forever(speed_sp=300)
            elif cont == 2:
                motorPorta.run_forever(speed_sp=-100)
            elif cont == 3:
                motorEsquerdo.run_forever(speed_sp=-300)
                motorDireito.run_forever(speed_sp=-300)
            elif cont == 4:
                motorDireito.run_to_abs_pos(position_sp=posicao_motor_D - 600, speed_sp=100)
                motorEsquerdo.run_to_abs_pos(position_sp=posicao_motor_E + 600, speed_sp=100)

        cont += 1
    
