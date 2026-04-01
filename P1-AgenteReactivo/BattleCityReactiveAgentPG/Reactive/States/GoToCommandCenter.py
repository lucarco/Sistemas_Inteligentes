from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class GoToCommandCenter(State):

    def __init__(self, id):
        super().__init__(id)
        self.Reset()

    def Update(self, perception, map, agent):

        """
        #Comportamiento agente Tonto:
        self.updateTime += perception[AgentConsts.TIME]
        if self.updateTime > 1.0:
            self.Reset()
        """

        print("Mi posición:", perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y])
        print("Command Center:", perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y])

        #Comportamiento agente listo: MEJORAR TENIENDO EN CUENTA LAS DISTANCIAS 

        agente_x = perception[AgentConsts.AGENT_X]
        agente_y = perception[AgentConsts.AGENT_Y]

        destino_x = perception[AgentConsts.COMMAND_CENTER_X]
        destino_y = perception[AgentConsts.COMMAND_CENTER_Y]

        print("Vida : ", perception[AgentConsts.LIFE_X], " ", perception[AgentConsts.LIFE_Y])

        if perception[AgentConsts.HEALTH] == 1 and perception[AgentConsts.LIFE_X] > 0 and perception[AgentConsts.LIFE_Y] > 0 :
            destino_x = perception[AgentConsts.LIFE_X]
            destino_y = perception[AgentConsts.LIFE_Y] 
        elif destino_x <= 0 and destino_y <= 0 :
            destino_x = perception[AgentConsts.EXIT_X]
            destino_y = perception[AgentConsts.EXIT_Y]

        distancia_x = destino_x - agente_x   
        distancia_y = destino_y - agente_y

        action = AgentConsts.NO_MOVE
        disparar = False

        objeto = AgentConsts.NOTHING
        dist_objeto = 0

        if abs(distancia_x) > abs(distancia_y):
            if distancia_x > 0:
                action = AgentConsts.MOVE_RIGHT
                objeto = perception[AgentConsts.NEIGHBORHOOD_RIGHT]
                dist_objeto = perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT]
            else:
                action = AgentConsts.MOVE_LEFT 
                objeto = perception[AgentConsts.NEIGHBORHOOD_LEFT]
                dist_objeto = perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT]
        else:
            if distancia_y > 0:
                action = AgentConsts.MOVE_UP
                objeto = perception[AgentConsts.NEIGHBORHOOD_UP]
                dist_objeto = perception[AgentConsts.NEIGHBORHOOD_DIST_UP]
            else:
                action = AgentConsts.MOVE_DOWN
                objeto = perception[AgentConsts.NEIGHBORHOOD_DOWN]
                dist_objeto = perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN]
        
        print("Objeto: ", objeto)
        print("Distancia: ", dist_objeto)


        #Si se detecta un muro destructible a menos de 2 casillas
        #(NO DISPARO A MUCHA DISTANCIA PARA NO GASTAR BALAS POR SI VIENE UN ENEMIGO PODER DEFENDERME)
        if objeto == AgentConsts.BRICK and dist_objeto <= 2.0 : 
            print("¡Muro destructible detectado! DISPARANDO...")
            disparar = True

        #Si no se puede pasar porque hay una pared indestructible en la siguiente casilla
        elif objeto == AgentConsts.UNBREAKABLE and dist_objeto <= 1.0 : 
            print("¡Muro indestructible detectado! ESQUIVANDO...")

            #Si se está moviendo en el eje Y y detecta obstaculo se intentará mover en el eje X
            if action == AgentConsts.MOVE_UP or action == AgentConsts.MOVE_DOWN: 
                #Intentamos movernos en HORIZONTAL hacia donde esté libre o hacia donde pueda abrirme camino balazos 
                if distancia_x > 0: #Priorizamos ir a la DERECHA
                    if perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.NOTHING or perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.BRICK :
                        action = AgentConsts.MOVE_RIGHT
                        if perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.BRICK : disparar = True
                    elif perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.NOTHING or perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.BRICK :
                        action = AgentConsts.MOVE_LEFT
                        if perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.BRICK : disparar = True
                else: # Priorizamos ir a la IZQUIERDA
                    if perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.NOTHING or perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.BRICK :
                        action = AgentConsts.MOVE_LEFT
                        if perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.BRICK : disparar = True
                    elif perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.NOTHING or perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.BRICK :
                        action = AgentConsts.MOVE_RIGHT
                        if perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.BRICK : disparar = True
            
            #Si se está moviendo en el eje X y detecta obstaculo se intentará mover en el eje Y
            elif action == AgentConsts.MOVE_RIGHT or action == AgentConsts.MOVE_LEFT:
                #Intentamos movernos en HORIZONTAL hacia donde esté libre o hacia donde pueda abrirme camino balazos
                if distancia_y > 0: #Priorizamos ir arriba
                    if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.NOTHING or perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.BRICK :
                        action = AgentConsts.MOVE_UP
                        if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.BRICK : disparar = True
                    elif perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.NOTHING or perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.BRICK :
                        action = AgentConsts.MOVE_DOWN
                        if perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.BRICK : disparar = True
                else: #Priorizamos ir abajo
                    if perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.NOTHING or perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.BRICK :
                        action = AgentConsts.MOVE_DOWN
                        if perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.BRICK : disparar = True
                    elif perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.NOTHING or perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.BRICK :
                        action = AgentConsts.MOVE_UP
                        if perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.BRICK : disparar = True
     
        elif objeto == AgentConsts.COMMAND_CENTER :
            print("COMMAND CENTER A TIRO: DISPARAR !!!!!!!")
            disparar = True
        
        return action, disparar

    
    def Transit(self, perception, map):

        #Para pasar al estado defensa solo si detecta una amenaza a una distancia peligrosa de 6 casillas
        DISTANCIA_ALERTA = 9.0
        
        vista_arriba = perception[AgentConsts.NEIGHBORHOOD_UP]
        vista_abajo = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        vista_izq = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        vista_der = perception[AgentConsts.NEIGHBORHOOD_RIGHT]

        dist_arriba = perception[AgentConsts.NEIGHBORHOOD_DIST_UP]
        dist_abajo = perception[AgentConsts.NEIGHBORHOOD_DIST_DOWN]
        dist_izq = perception[AgentConsts.NEIGHBORHOOD_DIST_LEFT]
        dist_der = perception[AgentConsts.NEIGHBORHOOD_DIST_RIGHT]

        #Se comprueba si hay amenazas a una distancia de 6.0 casillas (SHELL = Bala, PLAYER = El tanque enemigo)
        peligro_arriba = (vista_arriba == AgentConsts.SHELL or vista_arriba == AgentConsts.PLAYER) and (dist_arriba < DISTANCIA_ALERTA)
        peligro_abajo = (vista_abajo == AgentConsts.SHELL or vista_abajo == AgentConsts.PLAYER) and (dist_abajo < DISTANCIA_ALERTA)
        peligro_izq = (vista_izq == AgentConsts.SHELL or vista_izq == AgentConsts.PLAYER) and (dist_izq < DISTANCIA_ALERTA)
        peligro_der = (vista_der == AgentConsts.SHELL or vista_der == AgentConsts.PLAYER) and (dist_der < DISTANCIA_ALERTA)

        if peligro_arriba or peligro_abajo or peligro_izq or peligro_der :
            print("¡PELIGRO DETECTADO! Cambiando a Modo Defensa...")
            return "Defense"  
        
        return "GoToCommandCenter"
    
    def Reset(self):
        self.action = random.randint(1,4)
        self.updateTime = 0

