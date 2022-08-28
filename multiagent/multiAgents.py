# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from cmath import inf
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        capsules =successorGameState.getCapsules()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        #food 
        food_list = newFood.asList()
        food_dis =[util.manhattanDistance(newPos,food) for food in food_list]
        food_value = 0
        if len(food_dis)==0:
            food_value =0
        else:
            food_value = min(food_dis)

        # capsules
        capsule_dis =[util.manhattanDistance(newPos,capsule) for capsule in capsules]
        capsule_value=0
        if len(capsule_dis)==0:
            capsule_value =0
        else:
            capsule_value = min(capsule_dis)

        #closest ghost
        close_ghost_distance =util.manhattanDistance(newPos,newGhostStates[0].getPosition())
        for index, ghost in enumerate (newGhostStates):
            ghost_distance = util.manhattanDistance(newPos,ghost.getPosition())
            if ghost_distance <close_ghost_distance:
                close_ghost_distance=ghost_distance


        # ghost_one_position = newGhostStates[0].getPosition()
        # dis_one = util.manhattanDistance(newPos, ghost_one_position)
        # ghost_two_position =newGhostStates[1].getPosition()
        # dis_two = util.manhattanDistance(newPos, ghost_two_position)
        # if dis_one>dis_two:
        #     close_ghost = dis_two
        #     far_ghost = dis_one
        # else:
        #     close_ghost = dis_one
        #     far_ghost = dis_two

        eval =0

        if newScaredTimes[0]>0:
            eval = successorGameState.getScore() -close_ghost_distance/(food_value+1)
        else:    
            eval = successorGameState.getScore() +close_ghost_distance/(food_value+1)-capsule_value

        #Stop
        if action =="Stop":
            eval -=100

        return eval

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        val = self.getValue(gameState, 0)
        
        return val[0]


    def maxValue(self, gameState:GameState,depth):
        agentIndex =depth%gameState.getNumAgents()
        pacman_actions =gameState.getLegalActions(agentIndex)
        max_result,max_action = -inf,None

        if len(pacman_actions)==0:
            return self.evaluationFunction(gameState),None
    
        for action in pacman_actions:
            succ = gameState.generateSuccessor(agentIndex,action)
            result = self.getValue(succ, depth+1)

            if result[1]>max_result:
                max_result=result[1]
                max_action =action
        return max_action,max_result

    def minValue(self, gameState:GameState, depth):
        agentIndex =depth%gameState.getNumAgents()
        pacman_actions =gameState.getLegalActions(agentIndex)
        min_result, min_action =inf,None

        if len(pacman_actions)==0:
            return self.evaluationFunction(gameState),None

        for action in pacman_actions:
            succ = gameState.generateSuccessor(agentIndex,action)
            result = self.getValue(succ, depth+1)
            if result[1]<min_result:
                min_result = result[1]
                min_action =action
        return min_action,min_result


    def getValue (self,gameState:GameState,depth):
        pacman_actions =gameState.getLegalActions(0)
        if  depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose(): #evaluate the state, no need to get successors
            return None,self.evaluationFunction(gameState)
        elif depth%gameState.getNumAgents()==0: #pacman, maxValue
            return self.maxValue (gameState,depth)
        else: #agent, minValue
            return self.minValue(gameState,depth)








class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        val = self.getValue(gameState, 0, -float("inf"), float("inf"))
        return val[0]

    def maxValue(self, gameState:GameState,depth, alpha,beta):
        agentIndex =depth%gameState.getNumAgents()
        pacman_actions =gameState.getLegalActions(agentIndex)
        max_result,max_action = -inf,None

        if len(pacman_actions)==0:
            return self.evaluationFunction(gameState),None
    
        for action in pacman_actions:
            succ = gameState.generateSuccessor(agentIndex,action)
            result = self.getValue(succ, depth+1,alpha,beta)

            if result[1]>max_result:
                max_result=result[1]
                max_action =action
        
            if max_result > beta:
                return max_action, max_result
            
            alpha = max(alpha, max_result)

        return max_action,max_result

    def minValue(self, gameState:GameState, depth, alpha, beta):
        agentIndex =depth%gameState.getNumAgents()
        pacman_actions =gameState.getLegalActions(agentIndex)
        min_result, min_action =inf,None

        if len(pacman_actions)==0:
            return self.evaluationFunction(gameState),None

        for action in pacman_actions:
            succ = gameState.generateSuccessor(agentIndex,action)
            result = self.getValue(succ, depth+1,alpha,beta)
            if result[1]<min_result:
                min_result = result[1]
                min_action =action

            if min_result < alpha:
                return  min_action,min_result
            
            beta = min(beta, min_result)

        return min_action,min_result

    def getValue (self,gameState:GameState,depth, alpha, beta):
        pacman_actions =gameState.getLegalActions(0)
        if  depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose(): #evaluate the state, no need to get successors
            return None,self.evaluationFunction(gameState)
        elif depth%gameState.getNumAgents()==0: #pacman, maxValue
            return self.maxValue (gameState,depth,alpha,beta)
        else: #agent, minValue
            return self.minValue(gameState,depth, alpha, beta)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        val = self.getValue(gameState, 0)
        return val[0]
    
    def maxValue(self, gameState:GameState,depth):
        agentIndex =depth%gameState.getNumAgents()
        pacman_actions =gameState.getLegalActions(agentIndex)
        max_result,max_action = -inf,None

        if len(pacman_actions)==0:
            return self.evaluationFunction(gameState),None
    
        for action in pacman_actions:
            succ = gameState.generateSuccessor(agentIndex,action)
            result = self.getValue(succ, depth+1)
            if result[1]>max_result:
                max_result=result[1]
                max_action =action
        return max_action,max_result

    def chanceValue(self, gameState:GameState, depth):
        agentIndex =depth%gameState.getNumAgents()
        pacman_actions =gameState.getLegalActions(agentIndex)
       
        if len(pacman_actions)==0:
            return self.evaluationFunction(gameState),None
        chance_result =0
        
        for action in pacman_actions:
            p = float(1/len(pacman_actions))
            succ = gameState.generateSuccessor(agentIndex,action)
            chance_result+=p*self.getValue(succ,depth+1)[1]
        # index =random.randint(0, len(pacman_actions)-1)
        # chance_action = pacman_actions[index]
        # succ = gameState.generateSuccessor(agentIndex,chance_action)
        # chance_result =self.getValue(succ,depth+1)[1]

        return None,chance_result


    def getValue (self,gameState:GameState,depth):
        pacman_actions =gameState.getLegalActions(0)
        if  depth==self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose(): #evaluate the state, no need to get successors
            return (1,self.evaluationFunction(gameState))
        elif depth%gameState.getNumAgents()==0:#pacman, maxValue
            return self.maxValue (gameState,depth)
        else: #agent, minValue
            return self.chanceValue(gameState,depth)




def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    capsules =currentGameState.getCapsules()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

       
    #food 
    food_list = newFood.asList()
    food_dis =[util.manhattanDistance(newPos,food) for food in food_list]
    food_value = 0
    if len(food_dis)==0:
        food_value =0
    else:
        food_value = min(food_dis)

    # capsules
    capsule_dis =[util.manhattanDistance(newPos,capsule) for capsule in capsules]
    capsule_value=0
    if len(capsule_dis)==0:
        capsule_value =0
    else:
        capsule_value = min(capsule_dis)

    #closest ghost
    close_ghost_distance =util.manhattanDistance(newPos,ghostStates[0].getPosition())
    for index, ghost in enumerate (ghostStates):
        ghost_distance = util.manhattanDistance(newPos,ghost.getPosition())
        if ghost_distance <close_ghost_distance:
            close_ghost_distance=ghost_distance

    eval =0

    if scaredTimes[0]>0:
        eval = currentGameState.getScore() -close_ghost_distance/(food_value+1)
    else:    
        eval = currentGameState.getScore() +close_ghost_distance/(food_value+1.5)-capsule_value

    # print(currentGameState.getPacmanState())
    
    #Stop
    # if action =="Stop":
    #     eval -=100

    return eval

# Abbreviation
better = betterEvaluationFunction
