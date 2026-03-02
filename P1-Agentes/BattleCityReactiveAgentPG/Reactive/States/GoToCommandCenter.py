from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random


class GoToCommandCenter(State):

    def __init__(self, id):
        super().__init__(id)
        ##self.Reset()

    def Update(self,perception, map, agent):
        cc_x = perception[AgentConsts.COMMAND_CENTER_X]
        cc_y = perception[AgentConsts.COMMAND_CENTER_Y]

        dif_x = perception[AgentConsts.AGENT_X] - cc_x
        dif_y = perception[AgentConsts.AGENT_Y] - cc_y

        ## damos a suponer que la esquina inferior izq de la pantalla es el (0,0)
        #NOTHING = 0, MOVE_UP = 1, MOVE_DOWN = 2, MOVE_RIGHT = 3, MOVE_LEFT = 4
        # NOTHING = 0, UNBREAKABLE = 1, BRICK = 2, COMMAND_CENTER = 3, PLAYER = 4, SHELL = 5, OTHER = 6

        if abs(dif_x) > abs(dif_y) :
            done = False
            if dif_x < 0 :
                if(perception[AgentConsts.NEIGHBORHOOD_RIGHT] != 1):
                    self.action = AgentConsts.MOVE_RIGHT
                    done = True
            else :
                if(perception[AgentConsts.NEIGHBORHOOD_LEFT] != 1):
                    self.action = AgentConsts.MOVE_LEFT
                    done = True
        if(dif_y != 0) and done == False :
            if dif_y < 0 :
                self.action = AgentConsts.MOVE_UP
            else :
                self.action = AgentConsts.MOVE_DOWN
    
        return self.action, True


    
    def Transit(self,perception, map):
        return self.id
    
    def Reset(self):
        #self.action = random.randint(1,4)
        #self.updateTime = 0
        pass

""""
    def Update(self, perception, map, agent):
        self.updateTime += perception[AgentConsts.TIME]
        if self.updateTime > 1.0:
            self.Reset()
        return self.action,True
    
    def Transit(self,perception, map):
        return self.id
    

    def Reset(self):
        self.action = random.randint(1,4)
        self.updateTime = 0
        """