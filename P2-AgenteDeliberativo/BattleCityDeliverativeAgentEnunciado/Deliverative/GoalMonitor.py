import random
from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    GOAL_EXIT = 3
    
    def __init__(self, problem, goals, finalGoal):
        self.goals = goals
        self.finalGoal = finalGoal
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        self.recalculate = True

    def NeedReplaning(self, perception, map, agent):
        if self.recalculate:
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True
        
        currentGoal = self.problem.GetGoal()
        if currentGoal is None:
            print("REPLAN: goal es None")
            return True
        newGoal = self.SelectGoal(perception, map, agent)
        if newGoal.value != currentGoal.value:
            self.lastTime = perception[AgentConsts.TIME]
            print("REPLAN: cambio de meta", currentGoal.value, "->", newGoal.value)
            return True
        return False  
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):

        #TODO definir la estrategia del cambio de meta
        # print("TODO aqui faltan cosas :)")
 
        # 1. Solo nos queda una vida y hay vida accesible => objetivo ir hacia la vida
        if perception[AgentConsts.HEALTH] <= 1 and perception[AgentConsts.LIFE_X] != -1 and perception[AgentConsts.LIFE_Y] != -1:
            return self.goals[self.GOAL_LIFE]
        
        # 2. Vamos hacia el jugador porq detectamos que se encuentra a una distancia peligrosa
        playerX = perception[AgentConsts.PLAYER_X]
        playerY = perception[AgentConsts.PLAYER_Y]
        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]
        dist_al_jugador = abs(agentX - playerX) + abs(agentY - playerY)
        #Si se detecta al jugador y se detecta a una distancia "Peligrosa" ej. 10 casillas
        if playerX != -1 and playerY != -1 and dist_al_jugador < 10.0: 
            return self.goals[self.GOAL_PLAYER]
        
        # 3. vamos al CC
        if perception[AgentConsts.COMMAND_CENTER_X] != -1 and perception[AgentConsts.COMMAND_CENTER_Y] != -1:
            return self.goals[self.GOAL_COMMAND_CENTRER]
        
        # 4. vamos al Exit
        return self.finalGoal
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
