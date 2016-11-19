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
from matplotlib.font_manager import path


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class Node:
	"""
	This class creates a node structure which contains the information of 
	path, state and cost
	"""
    def __init__(self,path,state,cost):
        self.path = path
        self.state = state
        self.cost = cost
     
    def getState(self):
		"""
		returns the the state of this node
		"""
        return self.state
     
    def getPath(self):
		"""
		returns the path of this node
		"""
        return self.path
     
    def getCost(self):
		"""
		returns the cost of this node
		"""
        return self.cost
    

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
    initialPath = []
    initialState = problem.getStartState()
    initialCost = 0
    myNode = Node(initialPath, initialState, initialCost)
    if problem.isGoalState(myNode.getState()):
        return myNode.getPath()
    frontier = util.Stack()
    frontier.push(myNode)
    exploredSet = set([])
    
    while 1:
        if frontier.isEmpty():
            return []
        node = frontier.pop()
        if problem.isGoalState(node.getState()):
            return node.getPath()
        exploredSet.add(node.getState())
        for triple in problem.getSuccessors(node.getState()):
            action = triple[1]
            state = triple[0]
            cost = triple[2]
            path = (list)(node.getPath())
            path.append(action)
            child = Node(path, state, cost)
            if child.getState() not in exploredSet:
                frontier.push(child)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    initialPath = []
    initialState = problem.getStartState()
    initialCost = 0
    myNode = Node(initialPath, initialState, initialCost)
    if problem.isGoalState(myNode.getState()):
        return myNode.getPath()
    frontier = util.Queue()
    frontier.push(myNode)
    exploredSet = []
    big = [myNode.getState()] 
    while 1:
        if frontier.isEmpty():
            return []
        node = frontier.pop()
        big.remove(node.getState())
        if problem.isGoalState(node.getState()):
            return node.getPath()
        exploredSet.append(node.getState())
        for triple in problem.getSuccessors(node.getState()):
            action = triple[1]
            state = triple[0]
            cost = triple[2]
            path = (list)(node.getPath())
            path.append(action)
            child = Node(path, state, cost)
            if ((child.getState() not in exploredSet) and (child.getState() not in big)):
                frontier.push(child)
                big.append(child.getState())
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    initialPath = []
    initialState = problem.getStartState()
    initialCost = problem.getCostOfActions(initialPath)
    myNode = Node(initialPath,initialState,initialCost)
    frontier = util.PriorityQueue()
    frontier.push(myNode, myNode.getCost())
    exploredSet = set([])
    while 1:
        if frontier.isEmpty():
            return []
        node = frontier.pop()
        if problem.isGoalState(node.getState()):
            return node.getPath()
        if node.getState() not in exploredSet:
            exploredSet.add(node.getState())
            for triple in problem.getSuccessors(node.getState()): 
                action = triple[1]
                state = triple[0]
                path = (list)(node.getPath())
                path.append(action)
                cost = problem.getCostOfActions(path)
                child = Node(path, state, cost)
                frontier.push(child, cost)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    initialPath = []
    initialState = problem.getStartState()
    h = heuristic(initialState,problem)
    initialCost = problem.getCostOfActions(initialPath) + h
    myNode = Node(initialPath,initialState,initialCost)
    frontier = util.PriorityQueue()
    frontier.push(myNode, myNode.getCost())
    exploredSet = []
    while 1:
        if frontier.isEmpty():
            return []
        node = frontier.pop()
        if problem.isGoalState(node.getState()):
            return node.getPath()
        if node.getState() not in exploredSet:
            exploredSet.append(node.getState())
            for triple in problem.getSuccessors(node.getState()): 
                action = triple[1]
                state = triple[0]
                path = (list)(node.getPath())
                path.append(action)
                h = heuristic(state,problem)
                cost = problem.getCostOfActions(path) + h
                child = Node(path, state,cost)
                frontier.push(child,cost)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


