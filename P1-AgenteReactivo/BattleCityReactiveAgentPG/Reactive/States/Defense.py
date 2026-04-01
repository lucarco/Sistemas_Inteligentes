from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Defense(State):

    def __init__(self, id):
        super().__init__(id)

    def Update(self, perception, map, agent):

        vista_arriba = perception[AgentConsts.NEIGHBORHOOD_UP]
        vista_abajo = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        vista_izq = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        vista_der = perception[AgentConsts.NEIGHBORHOOD_RIGHT]

        #Primero ver si puedo disparar
        puedo_disparar = perception[AgentConsts.CAN_FIRE]
        disparar = False
        accion = AgentConsts.NO_MOVE
        
        #Si puedo disparar, Girar hacia el objetivo para disparar (Sea bala enemiga o sea directamente el tanque enemigo)
        if puedo_disparar :
            print("Puedo disparar!!")
            if vista_arriba == AgentConsts.SHELL or vista_arriba == AgentConsts.PLAYER:
                accion = AgentConsts.MOVE_UP
                disparar = True
                print("Puedo disparar!! Disparando hacia Arriba: ", vista_arriba)
            elif vista_abajo == AgentConsts.SHELL or vista_abajo == AgentConsts.PLAYER:
                accion = AgentConsts.MOVE_DOWN
                disparar = True
                print("Puedo disparar!! Disparando hacia Abajo: ", vista_abajo)
            elif vista_izq == AgentConsts.SHELL or vista_izq == AgentConsts.PLAYER:
                accion = AgentConsts.MOVE_LEFT
                disparar = True
                print("Puedo disparar!! Disparando hacia Izq: ", vista_izq)
            elif vista_der == AgentConsts.SHELL or vista_der == AgentConsts.PLAYER:
                accion = AgentConsts.MOVE_RIGHT
                disparar = True
                print("Puedo disparar!! Disparando hacia Der: ", vista_der) 
        #Si no puedo disparar, compruebo si lo que me viene es una bala, para esquivarla (como último recurso )
        else :
            print("No puedo disparar :(")
            #Si me viene una bala por el eje X, intento esquivarla moviéndome o arriba o abajo            
            if vista_izq == AgentConsts.SHELL or vista_der == AgentConsts.SHELL:
                if vista_arriba == AgentConsts.NOTHING:
                    accion = AgentConsts.MOVE_UP
                    print("Esquivo yéndome hacia arriba")
                elif vista_abajo == AgentConsts.NOTHING:
                    accion = AgentConsts.MOVE_DOWN
                    print("Esquivo yéndome hacia abajo")
            #Si me viene una bala por el eje Y, intento esquivarla moviéndome o a la derecha o a la izquierda
            elif vista_arriba == AgentConsts.SHELL or vista_abajo == AgentConsts.SHELL:
                if vista_der == AgentConsts.NOTHING:
                    accion = AgentConsts.MOVE_RIGHT
                    print("Esquivo yéndome hacia Dercha")
                elif vista_izq == AgentConsts.NOTHING:
                    accion = AgentConsts.MOVE_LEFT
                    print("Esquivo yéndome hacia izquierda")

        #Si no puedo disparar, (Y EL OBJETO QUE SE DETECTA ES EL TANQUE ENEMIGO) -> vuelvo al estado GoToCommandCenter, no persigo al enemigo, mi prioridad es disparar al commandCenter
        
        return accion, disparar

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