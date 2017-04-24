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
import math
from game import Agent
import time
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
        print "the legal mcves are",legalMoves
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        print 'I am here'
        print successorGameState
        print newPos
        print newFood.asList()
        cloestFoodDistance = 99999
        for foodLocation in newFood.asList():
            toFoodDistance = manhattanDistance(newPos, foodLocation)
            print toFoodDistance
            if toFoodDistance < cloestFoodDistance:
                cloestFoodDistance = toFoodDistance
        # print newGhostStates
        # print newScaredTimes
        minDistanceToGhost = 99999
        for tempGhostState in newGhostStates:
            distanceToGhost = manhattanDistance(newPos, tempGhostState.getPosition())
            if distanceToGhost < minDistanceToGhost:
                minDistanceToGhost = distanceToGhost

        # print newScaredTimes
        print 1.0 / cloestFoodDistance
        if newScaredTimes[0] != 0:
            return currentGameState.getScore()
        else:
            return currentGameState.getScore() + math.sqrt(1+minDistanceToGhost)

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
        self.minUtility = -999999
        self.maxUtility = 999999


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def min_value(self, gameState, unexploredDepth, adversarialIndex):
        legalMoves = gameState.getLegalActions(adversarialIndex)
        unexploredDepth -= 1
        if gameState.isWin() or gameState.isLose() or unexploredDepth == 0:
            return (None, self.evaluationFunction(gameState))
        if adversarialIndex != gameState.getNumAgents()-1:
            nextAgentIndex = adversarialIndex + 1
            nextScores = []
            for nextAction in legalMoves:
                sccessorState = gameState.generateSuccessor(adversarialIndex, nextAction)
                (nextGhostAction, nextGhostBestScore) = self.min_value(sccessorState, unexploredDepth, nextAgentIndex)
                nextScores.append((nextAction, nextGhostBestScore))
            return min(nextScores, key=lambda k: k[1])
        else:
            nextScores = []
            for nextAction in legalMoves:
                sccessorState = gameState.generateSuccessor(adversarialIndex, nextAction)
                (nextPacmanAction, nextPacmanBestScore) = self.max_value(sccessorState, unexploredDepth)
                nextScores.append((nextAction, nextPacmanBestScore))
            return min(nextScores, key=lambda k: k[1])


    def max_value(self, gameState, unexploredDepth, adversarialIndex=1):
        legalMoves = gameState.getLegalActions()
        unexploredDepth -= 1
        # print "In Max..."
        # print legalMoves
        # print unexploredDepth
        # print 'end max...'
        # time.sleep(2)
        nextScores = []
        if gameState.isWin() or gameState.isLose() or unexploredDepth == 0:
            return (None, self.evaluationFunction(gameState))
        for nextAction in legalMoves:
            successorState = gameState.generateSuccessor(0, nextAction)
            nextScores.append(self.min_value(successorState, unexploredDepth, adversarialIndex)[1])
        bestScore = max(nextScores)
        bestIndices = [index for index in range(len(nextScores)) if nextScores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return (legalMoves[chosenIndex], bestScore)

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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """

        # "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        # legalMoves = gameState.getLegalActions()
        #
        # # Choose one of the best actions
        # numAgents = gameState.getNumAgents()
        # self.unexploredDepth = self.depth * numAgents + 1
        # scores = [self.min_value(gameState, action, numAgents-1) for action in legalMoves]
        # bestScore = max(scores)
        # bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        # print gameState.generateSuccessor()
        # print "unexploredDepth",self.depth*gameState.getNumAgents()+1
        # print gameState.getNumAgents()
        # print self.depth
        (action, bestScore) = self.max_value(gameState, self.depth*gameState.getNumAgents()+1)

        "Add more of your code here if you want to"

        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def min_value(self, alpha, beta, gameState, unexploredDepth, adversarialIndex):
        legalMoves = gameState.getLegalActions(adversarialIndex)
        unexploredDepth -= 1
        minUtility = self.maxUtility
        bestAction = None
        if gameState.isWin() or gameState.isLose() or unexploredDepth == 0:
            return (bestAction, self.evaluationFunction(gameState))
        if adversarialIndex != gameState.getNumAgents()-1:
            nextAgentIndex = adversarialIndex + 1
            nextScores = []
            for nextAction in legalMoves:
                sccessorState = gameState.generateSuccessor(adversarialIndex, nextAction)
                (nextGhostAction, nextGhostMinUtility) = self.min_value(alpha, beta, sccessorState, unexploredDepth, nextAgentIndex)
                nextScores.append((nextAction, nextGhostMinUtility))
                if minUtility > nextGhostMinUtility:
                    minUtility = nextGhostMinUtility
                    bestAction = nextAction
                if minUtility < alpha:
                    break
                if minUtility < beta:
                    beta = minUtility
            return (bestAction, minUtility)
        else:
            for nextAction in legalMoves:
                sccessorState = gameState.generateSuccessor(adversarialIndex, nextAction)
                (nextPacmanAction, nextPacmanMaxUtility) = self.max_value(alpha, beta, sccessorState, unexploredDepth)
                if minUtility > nextPacmanMaxUtility:
                    minUtility = nextPacmanMaxUtility
                    bestAction = nextAction
                if minUtility < alpha:
                    break
                if minUtility < beta:
                    beta = minUtility
            return (bestAction, minUtility)


    def max_value(self, alpha, beta, gameState, unexploredDepth, adversarialIndex=1):
        legalMoves = gameState.getLegalActions()
        unexploredDepth -= 1
        maxUtility = self.minUtility
        bestAction = None
        # print "In Max..."
        # print legalMoves
        # print unexploredDepth
        # print 'end max...'
        # time.sleep(2)
        nextScores = []
        if gameState.isWin() or gameState.isLose() or unexploredDepth == 0:
            return (bestAction, self.evaluationFunction(gameState))
        for nextAction in legalMoves:
            successorState = gameState.generateSuccessor(0, nextAction)
            (adversarialAction, adversarialUtility) = self.min_value(alpha, beta, successorState, unexploredDepth, adversarialIndex)
            if maxUtility < adversarialUtility:
                maxUtility = adversarialUtility
                bestAction = nextAction
            if maxUtility > beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility

        return (bestAction, maxUtility)
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        # "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        alpha = self.minUtility
        beta = self.maxUtility
        (bestAction, bestScore) = self.max_value(alpha, beta, gameState, self.depth * gameState.getNumAgents() + 1)
        return bestAction

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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

