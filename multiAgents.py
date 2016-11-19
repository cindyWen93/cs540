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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        myFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPosition = [ghostState.getPosition() for ghostState in newGhostStates]
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
   
        ghostDistance = []
        for ghostPosition in newGhostPosition:
            ghostDistance.append(( (newPos[0] - ghostPosition[0]) ** 2 + (newPos[1] - ghostPosition[1]) ** 2 ) + 1)
        if(ghostDistance):
            minGhostDistance = min(ghostDistance)
        else:
            minGhostDistance = 0
            
        foodDistance = []
        for foodPosition in myFood.asList():
            foodDistance.append(( (newPos[0] - foodPosition[0]) ** 2 + (newPos[1] - foodPosition[1]) ** 2 ) + 1 )
        if(foodDistance):
            minFoodDistance = min(foodDistance)
            maxFoodDistance = max(foodDistance)
        else:
            minFoodDistance = 1
            
        if(action == "Stop"):
            return 0;
   
        return (minGhostDistance/minFoodDistance)
        
        "*** YOUR CODE HERE ***"

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        myDepth = 1

        return self.minimaxFn(0, gameState, self.depth, myDepth)
     
    
    def minimaxFn(self,agentIndex, gameState, depth, myDepth):
        
        if(agentIndex == gameState.getNumAgents()):
            agentIndex = 0
            myDepth = myDepth + 1
        
        if(agentIndex == 0):
            return self.max(agentIndex, gameState, depth, myDepth )
        
        if(agentIndex != 0):
            return self.min(agentIndex, gameState, depth, myDepth)
  
    def min(self, agentIndex, gameState, depth, myDepth):
       
        
        moves = gameState.getLegalActions(agentIndex)
        
        if not (moves):
            return scoreEvaluationFunction(gameState)
        
        myScore = []
        for move in moves:
            myScore.append(self.minimaxFn(agentIndex + 1, gameState.generateSuccessor(agentIndex, move),depth, myDepth))
        
        minScore = min(myScore)
        return minScore;
    
        
    def max(self, agentIndex, gameState, depth, myDepth):
        
        if(myDepth == depth + 1):
            return scoreEvaluationFunction(gameState)
        
        moves = gameState.getLegalActions(agentIndex)
        
        if not (moves):
            return scoreEvaluationFunction(gameState)
        
        myScore = []
        for move in moves:
            myScore.append(self.minimaxFn(agentIndex + 1, gameState.generateSuccessor(agentIndex, move), depth, myDepth ))
        
        maxScore = max(myScore)
        maxScoreIndex = myScore.index(maxScore)
        bestMove = moves[maxScoreIndex]
        
        if(myDepth == 1):
            return bestMove
        else:
            return maxScore
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        myDepth = 1
        alpha = float("-inf")
        beta = float("inf")
        return self.ABFn(0, gameState, self.depth, myDepth,alpha, beta)
     
    
    def ABFn(self,agentIndex, gameState, depth, myDepth,alpha, beta):
        
        if(agentIndex == gameState.getNumAgents()):
            agentIndex = 0
            myDepth = myDepth + 1
        
        if(agentIndex == 0):
            return self.max(agentIndex, gameState, depth, myDepth, alpha, beta)
        
        if(agentIndex != 0):
            return self.min(agentIndex, gameState, depth, myDepth, alpha, beta)
  
    def min(self, agentIndex, gameState, depth, myDepth, alpha, beta):
       
        moves = gameState.getLegalActions(agentIndex)
        
        if not (moves):
            return scoreEvaluationFunction(gameState)
        
        myScore = float("+inf")
        myScoreList = []
        myScoreList.append(myScore)
        for move in moves:
            myScoreList.append(self.ABFn(agentIndex + 1, gameState.generateSuccessor(agentIndex, move), depth, myDepth, alpha, beta ))
            myScore = min(myScoreList)
            if myScore < alpha :
                return myScore
            if myScore < beta:
               beta = myScore

        return myScore
    
        
    def max(self, agentIndex, gameState, depth, myDepth, alpha, beta):
        
        if(myDepth == depth + 1):
            return scoreEvaluationFunction(gameState)
        
        moves = gameState.getLegalActions(agentIndex)
        
        if not (moves):
            return scoreEvaluationFunction(gameState)
        
        myScore = float("-inf")
        myScoreList = []
        myScoreList.append(myScore)
        myList = []
        for move in moves:
            myScoreList.append(self.ABFn(agentIndex + 1, gameState.generateSuccessor(agentIndex, move), depth, myDepth, alpha, beta ))
            myScore = max(myScoreList)
            myList.append(myScore)
            if myScore > beta :
                return myScore
            if myScore > alpha:
                alpha = myScore
        if(myDepth != 1):
            return myScore
        else:
            myScoreIndex = myList.index(myScore)
            return moves[myScoreIndex]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        myDepth = 1

        return self.expectimaxFn(0, gameState, self.depth, myDepth)
     
    
    def expectimaxFn(self,agentIndex, gameState, depth, myDepth):
        
        if(agentIndex == gameState.getNumAgents()):
            agentIndex = 0
            myDepth = myDepth + 1
        
        if(agentIndex == 0):
            return self.max(agentIndex, gameState, depth, myDepth )
        
        if(agentIndex != 0):
            return self.ave(agentIndex, gameState, depth, myDepth)
  
    def ave(self, agentIndex, gameState, depth, myDepth):
               
        moves = gameState.getLegalActions(agentIndex)
        
        if not (moves):
            return scoreEvaluationFunction(gameState)
        
        myScore = []
        for move in moves:
            myScore.append(self.expectimaxFn(agentIndex + 1, gameState.generateSuccessor(agentIndex, move),depth, myDepth))
        
        aveScore = sum(myScore)/len(myScore)
        return aveScore;
    
        
    def max(self, agentIndex, gameState, depth, myDepth):
        
        if(myDepth == depth + 1):
            return scoreEvaluationFunction(gameState)
        
        moves = gameState.getLegalActions(agentIndex)
        
        if not (moves):
            return scoreEvaluationFunction(gameState)
        
        myScore = []
        for move in moves:
            myScore.append(self.expectimaxFn(agentIndex + 1, gameState.generateSuccessor(agentIndex, move), depth, myDepth ))
        
        maxScore = max(myScore)
        maxScoreIndex = myScore.index(maxScore)
        bestMove = moves[maxScoreIndex]
        
        if(myDepth == 1):
            return bestMove
        else:
            return maxScore

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPosition = currentGameState.getPacmanPosition()
    
    ghostPositions = currentGameState.getGhostPositions()
    ghostPacmanDistanceList = []
    for ghostPosition in ghostPositions:
        ghostPacmanDistanceList.append(util.manhattanDistance(pacmanPosition, ghostPosition))
    minghostDistance = min(ghostPacmanDistanceList)
    
    index = ghostPacmanDistanceList.index(minghostDistance)
    
    
    capsulePositions = currentGameState.getCapsules()
    capsulePacmanDistanceList = []
    for capsulePosition in capsulePositions:
        capsulePacmanDistanceList.append(util.manhattanDistance(pacmanPosition, capsulePosition))
    mincapsuleDistance= min(capsulePacmanDistanceList)
    
    foodPositions = currentGameState.getFood().asList()
    foodPacmanDistanceList = []
    for foodPosition in foodPositions:
        foodPacmanDistanceList.append(util.manhattanDistance(pacmanPosition, foodPosition))
    minfoodDistance = min(foodPacmanDistanceList)
    
    ghostStates = currentGameState.getGhostStates()
    scaredTime = [ghostState.scaredTimer for ghostState in ghostStates]
    myScaredTime = scaredTime[index]
    
    return (minghostDistance*(1+myScaredTime))/(minfoodDistance + minCapsuleDistance)
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

