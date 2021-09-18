import search
import random

romania_map = {
    'Arad':{'Zerind':75, 'Sibiu':140, 'Timisoara':118},
    'Zerind':{'Arad': 75, 'Oradea': 71},
    'Bucharest':{'Urziceni':85, 'Pitesti':101, 'Giurgiu':90, 'Fagaras':211},
    'Craiova':{'Drobeta':120, 'Rimnicu Vilcea':146, 'Pitesti':138},
    'Drobeta':{'Mehadia':75, 'Craiova': 120},
    'Eforie':{'Hirsova':86},
    'Fagaras':{'Sibiu':99, 'Bucharest': 211},
    'Hirsova':{'Urziceni':98, 'Eforie': 86},
    'Iasi':{'Vaslui':92, 'Neamt':87},
    'Lugoj':{'Timisoara':111, 'Mehadia':70},
    'Oradea':{'Zerind':71, 'Sibiu':151},
    'Pitesti':{'Rimnicu Vilcea':97, 'Craiova': 138, 'Bucharest': 101},
    'Urziceni':{'Vaslui':142, 'Bucharest': 85, 'Hirsova': 98},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Sibiu': {'Oradea': 151, 'Arad': 140, 'Rimnicu Vilcea': 80, 'Fagaras': 99},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Pitesti': 97, 'Craiova': 146},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Giurgiu': {'Bucharest': 90},
    'Vaslui': {'Iasi': 92, 'Urziceni': 142},
    'Neamt': {'Iasi': 87}
}

HEURISTIC = [
    ['Arad', 336],
    ['Bucharest', 0],    
    ['Craiova', 160],
    ['Drobeta', 242],
    ['Fagaras', 176],
    ['Giurgiu', 77],
    ['Lugoj', 244],
    ['Oradea', 380],
    ['Pitesti', 100],
    ['Rimnicu Vilcea', 193],
    ['Sibiu', 253],
    ['Timisoara', 329],
    ['Urziceni', 80],
    ['Zerind', 374]
]

def heuristic(state):
    for i in HEURISTIC:
        if state.pos == i[0]:
            return i[1]
    return None
class MapState:
    """
    The Eight Queen puzzle challenges you to arrange 8 queens on 
    a modern chessboard such that no queen is attacking one or another

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__( self, pos):
        """
            room: each element represent whether room is Dirty (True) or Clean. 
            vacc: position of vacuum ( 0 for left, 1 for right )
            
        """
        self.pos = pos

    def __hash__(self):
        return hash(self.pos)


    def isGoal( self ):
        """
          Check if 8 queens puzzle has reached its goal.

          Queen must be placed in each collumn.
          
          Queen at column i will not attack queen(s) on the right.

        """
        return self.pos == 'Bucharest'

    def legalMoves( self ):
        return romania_map[self.pos].keys()
        
    def result(self, move):
        """
          Returns a new eight-queen puzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        """
        cost  = romania_map[self.pos][move]

        newState = MapState(move)

        return newState

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        return self.pos == other.pos

    # def __hash__(self):
    #     return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        s = self.pos
        return s

    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class MapProblem(search.SearchProblem):
    """
      Implementation of a Search Problem for the  Eight Queen domain

      Each state is represented by an instance of an eightQueen.
    """
    def __init__(self,puzzle):
        "Creates a new EightQueenSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return puzzle

    def isGoalState(self,state):
        return state.isGoal()

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, romania_map[state.pos][a]))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        total = 0
        for i in actions: total = total + romania_map[self.puzzle.pos][i]
        return total

if __name__ == '__main__':
    
    # puzzle = createRandomPuzzle()
    # print('A random puzzle:')
    # print(puzzle)
    puzzle = MapState('Arad')
    problem = MapProblem(puzzle)
    path = search.astar(problem,heuristic)
    print(puzzle)
    curr = puzzle
    i = 1
    for a in path:
        input("Press return for the next state...")   # wait for key stroke
        curr = curr.result(a)
        s = "move "
        print('After %d move%s:' % (i, ("", "s")[i>1]))
        print(curr)
        
        i += 1
