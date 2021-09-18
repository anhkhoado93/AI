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

REVERSE_PUSH = 0
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

class Node:
    def __init__(self, state, parent =None, action = None, step_cost = 0):
        self.state      = state
        self.parent     = parent
        self.action     = action
        # self.step_cost  = step_cost
        self.path_cost  = (0 if not parent else parent.path_cost + step_cost)
        self.depth      = (1 if not parent else parent.depth + 1)
    
    def __eq__(self, other): 
        return self.state == other.state
    
    def path(self):
        path = []
        curr = self.parent
        while curr:
            if curr.parent: path.insert(0, curr.action)
            curr = curr.parent
        path.append(self.action)
        return path



class GraphSearch:
    def __init__(self, problem, typ):
        self.problem = problem
        self.typ = typ

    def search(self, frontier, depth_limit = None):
        new_node = Node(self.problem.getStartState())
        frontier.push(new_node)

        explored = set()

        while not frontier.isEmpty():
            node    = frontier.pop()
            state   = node.state
            if depth_limit != None and \
                node.depth > depth_limit and \
                    frontier.isEmpty():
                return "cut_off"
            if self.problem.isGoalState(state):
                return node.path()
            explored.add(state)
            successor = self.problem.getSuccessors(state)

            if self.typ == 'dfs':
                successor = successor[::-1]
            
            for new_state, action, step_cost in successor:
                new_node = Node(new_state, node, action, step_cost)
                if new_node in frontier and \
                    self.typ in ['ucs', 'befs', 'astar']:
                    frontier.update(new_node)
                if new_state in explored or \
                    (self.typ != 'dfs' and new_node in frontier):
                    continue
                
                frontier.push(new_node)
        return []

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
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    return GraphSearch(problem, 'dfs').search(fringe)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    return GraphSearch(problem, 'bfs').search(fringe)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueueWithFunction(lambda node: node.path_cost)
    return GraphSearch(problem, 'ucs').search(fringe)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueueWithFunction(lambda node: node.path_cost + heuristic(node.state, problem))
    return GraphSearch(problem, 'astar').search(fringe)

def bestFirstSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueueWithFunction(lambda node: heuristic(node.state, problem))
    return GraphSearch(problem, 'befs').search(fringe)

def depthLimitedSearch(problem, limit):
    fringe = util.Stack()
    res = GraphSearch(problem, 'dls').search(fringe, limit)

    return res if type(res) == type([]) else []

def iterativeDeepeningSearch(problem):
    depth = 0
    while True:
        res = depthLimitedSearch(problem, depth)
        if res != 'cutoff': return res 
        depth  = depth + 1
    return res
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
befs = bestFirstSearch
