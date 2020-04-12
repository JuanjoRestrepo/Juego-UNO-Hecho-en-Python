# JUEGO UNO
# JUAN JOSE RESTREPO ROSERO
import os
import random
#from Ventana_init import *

def FqueClear():
    QueClear = input("Si va a jugar en celular presione 'Enter' \n\
Presione otra tecla y despues 'Enter' si lo hará en computador: ")
    return QueClear
    
#clear()
print("\n\n")
QueClear = FqueClear()


def clear():    
    if QueClear == "":
        print()
        print()
        os.system("clear")
    else:
        os.system("cls")
    return 0
clear()

def evaluarPaso(paso, jugador_deturno):
    #print("paso a jugador: ", paso)
    
        
    if (paso > 0) and (jugador_deturno + paso >= cant_jugadores): #solo hay que ver si al momento de sumarle el paso
        #se daña la cosa
        jugador_deturno = jugador_deturno - cant_jugadores #EVALUAR LA DISTANCIA AL ERROR
    if (paso < 0) and (jugador_deturno + paso < 0):
        jugador_deturno = cant_jugadores + jugador_deturno
    jugador_deturno += paso

    if abs(paso) >= 2: #EL SALTO SOLO FUNCIONA UNA VEZ, AQUI SE RESETEA
        paso = int(paso / 2)            #PASI ES 2 o -2 Y SE /2 para ser 1 o -1
    return [paso, jugador_deturno]



def efectos(carta, paso):    
    if carta[0] == 'salto':
        paso = paso * 2
    if carta[0] == 'reversa':
        paso = (-1) * paso
    return paso



def respuesta(carta, acum, jugador_deturno):
    if carta[0] == '+2':
        acum += 2
    if carta[0] == '+4':
        acum += 4
    activador = True
    cartaActiva = True
    while activador:
        respuesta_a_comer = (input("Tienes para responder? Escriba (1 = si, Otro numero = no) \n\
y luego presione 'Enter' para continuar: "))        
        
        if respuesta_a_comer != '1':
            for i in range(acum):
                barajasJugadores[jugador_deturno].append(barajaT.pop())
            acum = 0
            activador = False
            cartaActiva = False
            refresh(jugador_deturno)
            input("Perdiste el turno :/ \n\
'Enter' para continuar")
        else:
            cartaSnum = (input("Numero de la Carta a poner para contrarestar: "))            
            while (True):
                if cartaSnum != '':
                    
                    while ( len(cartaSnum) > 2 or 49 > ord(cartaSnum[0]) or ord(cartaSnum[0]) > 57)\
                          or 48 > ord(cartaSnum[len(cartaSnum)-1]) or ord(cartaSnum[len(cartaSnum)-1]) > 57:                        
                        print("Carta invalida. vuelva a intentar")                        
                        cartaSnum = (input("Carta a poner: "))  # desde 1
                        while cartaSnum == '':
                            print("Carta invalida. vuelva a intentar")                        
                            cartaSnum = (input("Carta a poner: "))  # de                        
                    
                    cartaSnum = int(cartaSnum)
                    if cartaSnum > len(barajasJugadores[jugador_deturno]):
                        print("El numero de carta seleccionado no existe. Vuelvalo a ingresar")
                        cartaSnum = (input("Carta a poner: "))  # desde 1    
                    else:
                        break
                else:
                    print("Carta invalida. vuelva a intentar")
                    cartaSnum = (input("Numero de la Carta a poner para contrarestar: "))
            cartaSnum = int(cartaSnum)
            
            while cartaSnum > len(barajasJugadores[jugador_deturno]) or cartaSnum < 1:
                print("El numero de carta seleccionado no existe. Vuelvalo a ingresar")
                cartaSnum = (input("Numero de la Carta a poner para contrarestar: "))
                while cartaSnum == '':
                    print ("respuesta invalida. Intente de nuevo")
                    cartaSnum = (input("Numero de la Carta a poner para contrarestar: "))            
                cartaSnum = int(cartaSnum)
            cartaS = barajasJugadores[jugador_deturno][cartaSnum - 1]
            if cartaS[0][0] == '+' or cartaS[0][1] == barajaJuego[len(barajaJuego) - 1][1]:
                barajaJuego.append(barajasJugadores[jugador_deturno].pop(cartaSnum - 1))
                activador = False
            elif cartaS[0][0] == '+' and cartaS[0][1] == barajaJuego[len(barajaJuego) - 1][1]:
                barajaJuego.append(barajasJugadores[jugador_deturno].pop(cartaSnum - 1))
                activador = False
            else:
                # raw_input('Carta Invalida para contrarestar ')
                input('Carta Invalida para contrarestar. Seleccione otra:  ')
                refresh(jugador_deturno)
    return [cartaActiva, acum]


def cartaPoner(jugador_deturno, answer, paso):
    ACTIVADOR = True
    contador = 0
    
     #       input()
    while ACTIVADOR:
        
        cartaSnum = (input("Carta a poner: "))  # desde 1    
        while (cartaSnum != ''):
                
            while len(cartaSnum) > 2 or 49 > ord(cartaSnum[0]) or ord(cartaSnum[0]) > 57 \
                          or 48 > ord(cartaSnum[len(cartaSnum)-1]) or ord(cartaSnum[len(cartaSnum)-1]) > 57:
                print("Carta invalida. vuelva a intentar")
                cartaSnum = (input("Carta a poner: "))  # desde 1
                if cartaSnum == '': break
                
            if cartaSnum != '':
                cartaSnum = int(cartaSnum)
                if cartaSnum > len(barajasJugadores[jugador_deturno]) or cartaSnum < 1:
                    print("El numero de carta seleccionado no existe. Vuelvalo a ingresar")
                    cartaSnum = (input("Carta a poner: "))  # desde 1    
                else:
                    break
            
                
        if cartaSnum != '':
            cartaS = barajasJugadores[jugador_deturno][cartaSnum - 1]  # carta uno sera index 0

            cartita = cartaS[0] + ' ' + cartaS[1]
            print('Mi Carta: ', cartita)
            print()

            if barajaJuego[len(barajaJuego) - 1][0] == cartaS[0] or \
               barajaJuego[len(barajaJuego) - 1][1] == cartaS[1] or \
                    cartaS[1] == "negro" or \
                    barajaJuego[len(barajaJuego) - 1][
                1] == "negro":  # si es posible se pone la carta
                barajaJuego.append(barajasJugadores[jugador_deturno].pop(cartaSnum - 1))
                ACTIVADOR = False
                answer = True
                paso = efectos(cartaS, paso)
                #inp = True
            else:
                print("La carta que seleccionaste no es valida")
                if contador == 1:
                    respuesta = (input("Desea elegir otra carta o pasar turno? Escriba (1 = elegir, Otro Numero = pasar) \n\
y luego presione 'Enter': "))
                    if respuesta != '1':
                        ACTIVADOR = False
                else:
                    respuesta = (input("Desea elegir otra carta o comer? Escriba (1 = elegir, Otro Numero = comer) \n\
y luego presione 'Enter':  "))
                    if respuesta != '1':
                        barajasJugadores[jugador_deturno].append(barajaT.pop())
                        contador = 1
                    

        else:
            
            if contador == 1:
                respuesta = input("Si desea pasar presione 'Enter' \n\
Sino, digite un numero y presione 'Enter': ")
                if respuesta == '':
                    ACTIVADOR = False
            else:
                respuesta = input("Si desea comer presione 'Enter' \n\
Sino, digite un numero y presione 'Enter': ")
                if respuesta == '':
                    barajasJugadores[jugador_deturno].append(barajaT.pop())
                    contador = 1
                    
        refresh(jugador_deturno)        
        
    return [answer, paso]

def Pcarta (jugador_deturno):
    cartita = barajaJuego[len(barajaJuego) - 1][0] + ' ' + barajaJuego[len(barajaJuego) - 1][1]
    print('Carta en baraja de juego: ', cartita)
    print()
    print('Jugador de turno #', jugador_deturno + 1)
    print()
    return 0

def refresh(jugador_deturno):
    # refrescar:
    clear()
    printear(jugador_deturno)
    # fin refresh
    Pcarta(jugador_deturno)
    return 0


def respcomodin(jugador_deturno):
    
    color = (input("Ingrese el color al que desea cambiar \n\
1 = azul, 2 = rojo \n\
3 = amarillo, 4 = verde : "))
                
    while color == '':
        refresh(jugador_deturno)
        print("Color incorrecto. Pruebe de nuevo")
        color = (input("Ingrese el color al que desea cambiar \n\
1 = azul, 2 = rojo \n\
3 = amarillo, 4 = verde : "))
                
    while ( len(color) != 1 or 49 > ord(color) or ord(color) > 52):
        refresh(jugador_deturno)
        print("Color incorrecto. Pruebe de nuevo")
        color = (input("Ingrese el color al que desea cambiar \n\
1 = azul, 2 = rojo \n\
3 = amarillo, 4 = verde : "))

        while color == '':
            refresh(jugador_deturno)
            print("Color incorrecto. Pruebe de nuevo")
            color = (input("Ingrese el color al que desea cambiar \n\
1 = azul, 2 = rojo \n\
3 = amarillo, 4 = verde : "))
                
    color = int(color)

    # colores de la lista colores, se resta -1 al color que quiere cambiar
    # para que se tome el color deseado de la lista colores
    barajaJuego[len(barajaJuego) - 1][1] = colores[color - 1]
    return 0




# LO PRRRIMERRRROOOO
# Crear baraja
numeros_y_especiales = ["0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5",
                        "6", "6", "7", "7", "8", "8", "9", "9",
                        "+2", "+2", "salto", "salto", "reversa", "reversa"]

colores = ["azul", "rojo", "amarillo", "verde"]

barajaT = []
#barajasJugadores = []  # BARAJAS DE LOS JUGADORES
#barajaJuego = []

comodines = ["+4", "comodin"]

for n in numeros_y_especiales:
    for c in colores:
        # indicador de carta en posicion cero y color en posicion 1
        carta = [n, c]
        barajaT.append(carta)

for com in comodines:
    for i in range(4):
        carta = [com, "negro"]  # indicador de carta en posicion cero y color en posicion 1
        barajaT.append(carta)

random.shuffle(barajaT)
'''
# muestra baraja aleatoria
print()
print("Baraja Completa")
print()
for m in range(len(barajaT)):
   for n in range(len(barajaT[m])):  
       print(barajaT[m][n],"",end="")                                         
   print()      
'''

print()


# lista para las barajas de cada jugador

barajasJugadores = []  # BARAJAS DE LOS JUGADORES
#barajaJuego = []

# Repartiendo 7 cartas a 4 jugadores (28 en total)

# digitar la cantidad de jugadores

cant_jugadores = (input("Ingrese el Numero de Jugadores: "))



while (True):
    if cant_jugadores != '':
        
        while ( len(cant_jugadores) != 1 or 50 > ord(cant_jugadores[0]) or ord(cant_jugadores[0]) > 54):
            print("La cantidad de jugadores debe ser mayor a 1 o menor a 7")
            cant_jugadores = (input("Ingrese el Numero de jugadores: "))  # desde 1
            
        if cant_jugadores != '':
            break
        else:
            print("Numero invalido. Vuelva a ingresar¡")
            cant_jugadores = (input("Ingrese el Numero de jugadores: "))  # desde 1
    else:
        print("La cantidad de jugadores debe ser mayor a 1 o menor a 7")
        cant_jugadores = (input("Ingrese el Numero de jugadores: "))
cant_jugadores = int(cant_jugadores)


# ciclo para meter una lista vacia (la baraja de cada jugador)
for i in range(cant_jugadores):
    barajasJugadores.append([])

# meter cartas en lista de baraja de cada jugador
for i in range(7):
    for j in range(cant_jugadores):
        carta = barajaT.pop()  # pop para sacar cartas de la baraja. No elimina del sistema
        barajasJugadores[j].append(carta)


# Mostrando las cartas de cada jugador
def printear(i):
    print()
    print("Numero Carta", " - ", "Tipo de Carta \n\
Ingrese el numero de la carta que desea poner" )
    print("Si no tiene carta para poner, presione 'Enter' dos veces")
    print()
    print("Jugador {}:".format(i + 1))

    for j in range(len(barajasJugadores[i])):
        cartita = barajasJugadores[i][j][0] + ' ' + barajasJugadores[i][j][1]
        print(j + 1," - ", "{:16}".format(cartita, end=""))
    print()

    return 0


"""#Mostrando las cartas restantes 

for i in range(0,len(barajaT)):
    print("{:17}".format(barajaT[i]))


#Carta Reversa"""

barajaJuego = []
barajaJuego.append(barajaT.pop())  # Sacar primera carta PA LA BARAJA DE JUEGO (INICIAR PARTIDA)


# print(barajaJuego[len(barajaJuego)-1])#-1 cambia index de cero a 1

def Fclaves(claves, jugador_deturno):
        
    clear()
    
    print("Jugador", jugador_deturno+1, " digite su clave y despues presione 'Enter': ")          
    clave_cadajugador = (input()) 
    clear()
    
    while claves[jugador_deturno] != clave_cadajugador:
        print("Jugador", jugador_deturno + 1,"ha digitado una clave errada.\
\n Digite su clave de nuevo: ")          
        clave_cadajugador = (input()) 
        clear()
    
    refresh(jugador_deturno)
    
    return 0

# Desarrollo del juego
def inicializador ():
    UNO = True

    claves = []
    x=0
    acum = 0
    paso = 1
    answer = True        
    
    clear()
    for x in range(cant_jugadores):
        print("Jugador", x+1, " digite su clave y despues presione 'Enter': ")          
        clave_cadajugador = (input()) 
        claves.append(clave_cadajugador)
        clear()     

    jugador_deturno = random.randint(0, cant_jugadores - 1)  # seleccion al azar del primer jugador

    print("El primer jugador es el", jugador_deturno + 1, "\n\
Presione 'Enter' para continuar. "),    input ()

    if barajaJuego[len(barajaJuego) - 1][0][0] == 's':
        Pcarta(jugador_deturno)
        input()
        efectos(carta, paso)
        [paso, jugador_deturno] = evaluarPaso(paso, jugador_deturno)
    return [claves, UNO, acum, paso, answer, jugador_deturno] 


def Desarrollo (answer, acum, jugador_deturno, paso):
    if barajaJuego[len(barajaJuego) - 1][0][0] == '+' and answer:            # AQUI SE ACTUALIZA EL ACUM
        [answer, acum] = respuesta(barajaJuego[len(barajaJuego) - 1], acum, jugador_deturno)
            #se desactiva el answer = False (la carta en juego )
    else:            
        [answer, paso] = cartaPoner(jugador_deturno, answer, paso)          # carta que el jugador va a poner en la barajaJuego
            #answer = True solo cuando alguien haya puesto una carta
    if barajaJuego[len(barajaJuego) - 1][1] == 'negro':
        respcomodin(jugador_deturno)

    return [answer, acum, jugador_deturno, paso]



#barajaT = []
#barajasJugadores = []  # BARAJAS DE LOS JUGADORES
#barajaJuego = []
    
def GanarOreset(jugador_deturno, acum, UNO): #, barajaT
    if len(barajasJugadores[jugador_deturno]) == 0:
        clear()
        print()
        print("El jugador ",jugador_deturno + 1," ha ganado!!!!!  :) ")
        print("Presione 'Enter' para continuar")
        print()
        input()
        UNO = False
    

    if (len(barajaT) == acum+4):
        #print("hola")
        
        x = barajaJuego.pop()
        while len(barajaJuego) > 0:
            barajaT.append(barajaJuego.pop())    
        
        barajaJuego.append (x)
        random.shuffle(barajaT)        
        print("Reset"), input()#'''
    else: print ("Quedan ",len(barajaT)," cartas en la baraja para comer ","\n\
Hay ",len(barajaJuego)," cartas en la baraja de juego","\n\
Presione 'Enter' para continuar: ") , input()    #Para verificar
    
    return UNO

    
    
def main():
    
    [claves, UNO, acum, paso, answer, jugador_deturno] = inicializador ()
    
    while UNO:

        Fclaves(claves, jugador_deturno)
            
        [answer, acum, jugador_deturno, paso] = Desarrollo (answer, acum, jugador_deturno, paso)

        UNO = GanarOreset(jugador_deturno, acum, UNO) #
                                
        [paso, jugador_deturno] = evaluarPaso(paso, jugador_deturno)
        

    return 0


main()
