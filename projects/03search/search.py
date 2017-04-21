# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import time
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# def isAllSuccessorsExplored(currentState, exploredStateSet, problem):
#     allSuccessorsExploredFlag = True
#     for nextStateInfo in problem.getSuccessors(currentState):
#         if not(nextStateInfo[0] in exploredStateSet):
#             allSuccessorsExploredFlag = False
#             break
#     return allSuccessorsExploredFlag
#
# def addOneNode(nodeDict, currentState, parentState):
#     nodeDict[currentState] = {'parentState': parentState}


class Node(object):
    def __init__(self, state, fromAction, fromCost, parent):
        self.state = state
        self.fromAction = fromAction
        self.fromCost = fromCost
        if parent == None:
            self.costSoFar = fromCost
        else:
            self.costSoFar = parent.getCostSoFar() + fromCost
        self.parent = parent
    def getState(self):
        return self.state
    def getFromAction(self):
        return self.fromAction
    def getParentNode(self):
        return self.parent
    def getCostSoFar(self):
        return self.costSoFar

class generalSolver(object):
    def __init__(self, problem, searchType='dfs', heuristic=nullHeuristic):
        self.pathSeq = []
        self.totalPathCost = 0
        self.nodeDict = {}
        self.fringeStateSet = set()
        self.exploredStateSet = set()
        self.usePriority = False
        self.heuristic = heuristic
        self.problem = problem
        if searchType == 'astar':
            self.fringe = util.PriorityQueue()
            self.usePriority = True
        elif searchType == 'ucs':
            self.fringe = util.PriorityQueue()
            self.usePriority = True
        elif searchType == 'bfs':
            self.fringe = util.Queue()
        else:
            self.fringe = util.Stack()
    def getNodeFromState(self, state):
        return self.nodeDict[state]
    def addNode(self, state, fromAction, fromCost, parent):
        newNode = Node(state, fromAction, fromCost, parent)
        self.nodeDict[state] = newNode
        return newNode

    def fringePush(self, newNode):
        if self.usePriority:
            self.fringe.push(newNode.getState(), newNode.getCostSoFar() + self.heuristic(newNode.getState(), self.problem))
        else:
            self.fringe.push(newNode.getState())
        self.nodeDict[newNode.getState()] = newNode
        self.fringeStateSet.add(newNode.getState())
    # def fringeUpdate(self, newNode):
    #     self.fringe.update
    def fringePop(self):
        state = self.fringe.pop()
        self.fringeStateSet.remove(state)
        return self.nodeDict[state]
    def fringeUpdate(self, newNode):
        self.nodeDict[newNode.getState()] = newNode
        self.fringe.update(newNode.getState(), newNode.getCostSoFar() + self.heuristic(newNode.getState(), self.problem))
    def isEmptyFringe(self):
        return self.fringe.isEmpty()


    def getPathToGoalNode(self, goalNode):
        self.totalPathCost = goalNode.getCostSoFar()
        while goalNode:
            goalState = goalNode.getState()
            fromAction = self.nodeDict[goalState].getFromAction()
            if fromAction != None:
                self.pathSeq.append(fromAction)

            goalNode = self.nodeDict[goalState].getParentNode()


        self.pathSeq.reverse()
        print "the path is ",self.pathSeq
        return self.pathSeq

    def isNodeInFringe(self, node):
        return node.getState() in self.fringeStateSet
    def isNodeExplored(self, node):
        return node.getState() in self.exploredStateSet

    def makeExploredNode(self, node):
        self.exploredStateSet.add(node.getState())

    def solveProblem(self):
        startState = self.problem.getStartState()
        startNode = Node(startState, None, 0, None)
        self.fringePush(startNode)

        while not self.isEmptyFringe():
            currentNode = self.fringePop()
            # print "Is the start a goal?", self.problem.isGoalState(currentNode.getState()),currentNode.getState()

            if self.problem.isGoalState(currentNode.getState()):
                goalPath = self.getPathToGoalNode(currentNode)

                print "goal path length is ",len(goalPath)
                return goalPath
            print currentNode.getState()
            print currentNode.getCostSoFar()
            self.makeExploredNode(currentNode)
            for (toState, fromAction, fromCost) in self.problem.getSuccessors(currentNode.getState()):
                # print(toState, fromAction, fromCost)
                tempNode = Node(toState, fromAction, fromCost,currentNode)
                if not(self.isNodeExplored(tempNode) or self.isNodeInFringe(tempNode)):
                    newNode = Node(toState, fromAction, fromCost, currentNode)
                    self.fringePush(newNode)
                elif tempNode.getCostSoFar() < self.nodeDict[toState].getCostSoFar():
                    self.fringeUpdate(tempNode)
        print  "Can't not find a path to the goal state!!!"
        return []







# def graphSearch(problem, fringeFuc):
#     fringe = fringeFuc()
#     startState = problem.getStartState()
#     startStateInfo = (startState, None, 1)
#     depthFringe = util.Stack()
#     fringeStateSet = set()
#     actionSeq = []
#     nodeDict = {}
#     addOneNode(nodeDict, startState, None)
#     depthFringe.push(startStateInfo)
#     fringeStateSet.add(startState)
#     exploredStateSet = set()



def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    # "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    dfsSearch = generalSolver(problem, 'dfs')
    return dfsSearch.solveProblem()

    # startState = problem.getStartState()
    # startStateInfo = (startState, None, 1)
    # depthFringe = util.Stack()
    # fringeStateSet = set()
    # actionSeq = []
    # nodeDict = {}
    # addOneNode(nodeDict, startState, None)
    # depthFringe.push(startStateInfo)
    # fringeStateSet.add(startState)
    # exploredStateSet = set()
    #
    # while not depthFringe.isEmpty():
    #     (currentState, useAction, currentCost) = depthFringe.pop()
    #     fringeStateSet.remove(currentState)
    #     if useAction != None:
    #         actionSeq.append(useAction)
    #     print currentState
    #     print "Is is a goal?", problem.isGoalState(currentState)
    #     if problem.isGoalState(currentState):
    #         print "path length is ", len(actionSeq)
    #         return actionSeq
    #
    #
    #     if currentState not in exploredStateSet:
    #         exploredStateSet.add(currentState)
    #         allSuccessorsExploredFlag = True
    #         for nextStateInfo in problem.getSuccessors(currentState):
    #             if not(nextStateInfo[0] in exploredStateSet or nextStateInfo[0] in fringeStateSet):
    #                 allSuccessorsExploredFlag = False
    #                 addOneNode(nodeDict, nextStateInfo[0], currentState)
    #                 depthFringe.push(nextStateInfo)
    #                 fringeStateSet.add(nextStateInfo[0])
    #
    #         # Tracebacking
    #         while allSuccessorsExploredFlag:
    #             curParentState = nodeDict[currentState]['parentState']
    #             for tempSuccInfo in problem.getSuccessors(currentState):
    #                 if tempSuccInfo[0] == curParentState:
    #                     actionSeq.append(tempSuccInfo[1])
    #                     currentState = tempSuccInfo[0]
    #                     break
    #             allSuccessorsExploredFlag = isAllSuccessorsExplored(currentState, exploredStateSet, problem)
    #
    #
    # return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # print "Start:", problem.getStartState()
    #
    # from game import Directions
    # oppsiteDirectionDict = {Directions.EAST:Directions.WEST, Directions.WEST:Directions.EAST, Directions.NORTH:Directions.SOUTH, Directions.SOUTH: Directions.NORTH}
    # startState = problem.getStartState()
    # startStateInfo = (startState, None, 0)
    # breadthFringe = util.Queue()
    # fringeStateSet = set()
    # actionSeq = []
    # nodeDict = {}
    # addOneNode(nodeDict, startState, None)
    # breadthFringe.push(startStateInfo)
    # fringeStateSet.add(startState)
    # exploredStateSet = set()
    # lastState = None
    # while not breadthFringe.isEmpty():
    #     (currentState, useAction, currentCost) = breadthFringe.pop()
    #     fringeStateSet.remove(currentState)
    #     # BackTracking
    #     lengthActionSeq = len(actionSeq)
    #     startIndex = lengthActionSeq - 1
    #     while startIndex >= 0 and lastState != None and nodeDict[currentState]['parentState'] != None and nodeDict[currentState]['parentState'] != lastState:
    #         backAction = oppsiteDirectionDict[actionSeq[startIndex]]
    #         for tempSuccInfo in problem.getSuccessors(lastState):
    #             if tempSuccInfo[1] == backAction:
    #                 actionSeq.append(backAction)
    #                 lastState = tempSuccInfo[0]
    #                 break
    #         startIndex -= 1
    #
    #     if useAction != None:
    #         actionSeq.append(useAction)
    #     print "Is is a goal?", problem.isGoalState(currentState)
    #     if problem.isGoalState(currentState):
    #         print "path length is ", len(actionSeq)
    #         return actionSeq
    #
    #     if currentState not in exploredStateSet:
    #         exploredStateSet.add(currentState)
    #         for nextStateInfo in problem.getSuccessors(currentState):
    #             if not(nextStateInfo[0] in exploredStateSet or nextStateInfo[0] in fringeStateSet):
    #                 addOneNode(nodeDict, nextStateInfo[0], currentState)
    #                 breadthFringe.push(nextStateInfo)
    #                 fringeStateSet.add(nextStateInfo[0])
    #     lastState = currentState
    #
    # return []
    bfsSearch = generalSolver(problem, 'bfs')
    return bfsSearch.solveProblem()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    ucsSearch = generalSolver(problem, 'ucs')
    return ucsSearch.solveProblem()

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    astarSearch = generalSolver(problem, 'astar', heuristic)
    return astarSearch.solveProblem()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
