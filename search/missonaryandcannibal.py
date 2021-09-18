import search
import random
# Module Classes




class MacState:
    """
    The Eight Queen puzzle challenges you to arrange 8 queens on 
    a modern chessboard such that no queen is attacking one or another

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__( self, no_missionary1 = 3,no_canibal1 = 3, no_missionary2 = 0, no_canibal2 = 0, direction = -1 ):
        """
            
        """
        self.m_side1 = no_missionary1
        self.m_side2 = no_missionary2
        self.c_side1 = no_canibal1
        self.c_side2 = no_canibal2
        self.direction = direction

    def isGoal( self ):
        """
          Check if 8 queens puzzle has reached its goal.

          Queen must be placed in each collumn.
          
          Queen at column i will not attack queen(s) on the right.

        """
        return self.m_side1 == 0 and self.c_side1 == 0


    def legalMoves( self ):
        """
        (m, c, dir)
        m:  num of missionary
        c:  num of cannibal
        dir: -1 == left, 1 == right
        """
        action = [
        (2,0,-1),
        (1,1,-1),
        (1,0,-1),
        (0,1,-1),
        (0,2,-1),
        (2,0, 1),
        (1,1, 1),
        (1,0, 1),
        (0,1, 1),
        (0,2, 1)
        ]
        ret = []
        for m, c, d in action:
            if  d == self.direction and \
                self.is_valid(self.m_side1 + m*d, self.c_side1 + c*d, self.m_side2 - m*d, self.c_side2 - c*d):
                ret.append((m,c,d))
        # if self.direction == 'left':
        #     action = action[:5]
        #     if not self.is_valid(self.m_side1 - 2, self.c_side1, self.m_side2 + 2, self.c_side2):
        #         action.remove("left_m_m")
        #     if not self.is_valid(self.m_side1 - 1, self.c_side1 - 1, self.m_side2 + 1, self.c_side2 + 1):
        #         action.remove("left_m_c")
        #     if not self.is_valid(self.m_side1 - 1, self.c_side1, self.m_side2 + 1, self.c_side2):
        #         action.remove("left_m")
        #     if not self.is_valid(self.m_side1, self.c_side1 - 1, self.m_side2, self.c_side2 + 1):
        #         action.remove("left_c")
        #     if not self.is_valid(self.m_side1, self.c_side1 - 2, self.m_side2, self.c_side2 + 2):
        #         action.remove("left_c_c")
        # else:
        #     action = action[5:]

        #     if not self.is_valid(self.m_side1 + 2, self.c_side1, self.m_side2 - 2, self.c_side2):
        #         action.remove("right_m_m")
        #     if not self.is_valid(self.m_side1 + 1, self.c_side1 + 1, self.m_side2 - 1, self.c_side2 - 1):
        #         action.remove("right_m_c")
        #     if not self.is_valid(self.m_side1 + 1, self.c_side1, self.m_side2 - 1, self.c_side2):
        #         action.remove("right_m")
        #     if not self.is_valid(self.m_side1, self.c_side1 + 1, self.m_side2, self.c_side2 - 1):
        #         action.remove("right_c")
        #     if not self.is_valid(self.m_side1, self.c_side1 + 2, self.m_side2, self.c_side2 - 2):
        #         action.remove("right_c_c")
        return ret


    def is_valid(self, m1, c1, m2, c2):
        if m1 < 0 | m2 < 0 | c1 < 0 | c2 < 0: return 0
        return (m1 >= c1 or m1 == 0) and (m2 >= c2 or m2 == 0)

    def __hash__(self):
        lst = (self.m_side1, self.m_side2, self.c_side1, self.c_side2, self.direction)
        return hash(lst)

    def result(self, move):
        """
          Returns a new eight-queen puzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        """
        # m = 0
        # c = 0
        # lst = move.split('_')
        # for i in range(1, len(lst)):
        #     if lst[i] == 'm': m = m + 1
        #     if lst[i] == 'c': c = c + 1
        # if lst[0] == 'left':
        #     m = -m
        #     c = -c

        # newDir = 'left' if self.direction == 'right' else 'right'
        # # print(self.m_side1 + m, self.c_side1 + c, self.m_side2 - m, self.c_side2 - c, newDir)
        m = move[0]
        c = move[1]
        d = move[2]
        newState = MacState(self.m_side1 + m * d, self.c_side1 + c * d, self.m_side2 - m * d, self.c_side2 - c * d, -d)

        return newState

    # Utilities for comparison and display
    def __eq__(self, other):
        """
        """
        return (self.m_side1 == other.m_side1 
            and self.m_side2 == other.m_side2
            and self.c_side1 == other.c_side1 
            and self.c_side2 == other.c_side2)

    # def __hash__(self):
    #     return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lst = []
        str1, str2 = "", ""
        for i in range(self.m_side1):  
            str1 = str1 + "m  "
        for i in range(self.c_side1):  
            str1 = str1 + "c  "
        for i in range(self.m_side2):  
            str2 = str2 + "m  "
        for i in range(self.c_side2):  
            str2 = str2 + "c  "
        lst.append(str1)
        lst.append("""\n~~~~~~~~~~~~~~~~~~\n~~~~~~~~~~~~~~~~~~\n""")
        lst.append(str2)
        return ''.join(lst)

    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class MacProblem(search.SearchProblem):
    """
      Implementation of a Search Problem for the  Eight Queen domain

      Each state is represented by an instance of an eightQueen.
    """
    def __init__(self,puzzle):
        "Creates a new EightQueenSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

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
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

if __name__ == '__main__':
    puzzle = MacState()
    problem = MacProblem(puzzle)
    path = search.breadthFirstSearch(problem)
    print(puzzle)
    print('BFS found a path of %d moves' % (len(path)))
    curr = puzzle
    i = 1
    for a in path:
        input("Press return for the next state...")   # wait for key stroke
        curr = curr.result(a)
        s = "move "
        print('After %d move%s: %s' % (i, ("", "s")[i>1], ()))
        print(curr)
        
        i += 1
