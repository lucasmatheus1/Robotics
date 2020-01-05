velIdeal = 500

cont = 0

bateriaIdeal = 80
carga = 80

while (cont < 100):

    carga -= 1
    if carga == 0:
        break

    valorSoma = bateriaIdeal - carga

    velocidade = 500+valorSoma

    print (velocidade)
    
    
    cont += 1
