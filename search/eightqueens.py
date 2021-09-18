import search
import random
# Module Classes

class EightQueenState:
    """
    The Eight Queen puzzle challenges you to arrange 8 queens on 
    a modern chessboard such that no queen is attacking one or another

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__( self ):
        """
            pos: store the queen position of each column.

            pos position of -1 indicate a queen has not
             been assigned
        """
        self.pos = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.cursor = 0


    def isGoal( self ):
        """
          Check if 8 queens puzzle has reached its goal.

          Queen must be placed in each collumn.
          
          Queen at column i will not attack queen(s) on the right.

        """
        if self.cursor != 8: return False

        for q1 in range( 8 ):
            for q2 in range( q1 + 1, 8 ):
                xDiff = q2 - q1
                yDiff = self.pos[q2] - self.pos[q1]
                if (yDiff == 0) | (abs(yDiff / xDiff) == 1):    
                    return False

        return True

    def legalMoves( self ):
        """
          Any cell of the left-most column that is not attacked by other queens
        """
        illegal_moves = [i for i in range(8)]
        # for i in range( self.cursor ):
        #     illegal_moves.append(self.pos[i])
        #     if (self.cursor - i) + self.pos[i] < 7:
        #         illegal_moves.append((self.cursor - i) + self.pos[i])

        # move = [i for i in range(8) if i not in illegal_moves]


        move = [i for i in range(8)]
        for i in range( self.cursor ):
            for e in illegal_moves:
                if e == self.pos[i]: 
                    if e in move: move.remove(e)
                if abs((self.cursor - i)) == abs(e - self.pos[i]):
                    if e in move: move.remove(e)

        return move

    def result(self, move):
        """
          Returns a new eight-queen puzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        """
        if move < 0 | move > 8: raise "Illegal move"

        newState = EightQueenState()
        newState.pos = self.pos[:]
        newState.cursor = self.cursor + 1

        newState.pos[self.cursor] = move

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
        ans = []
        for i in range(8):
            str = ""
            str = str + '|'
            for j in range(8):
                if self.pos[j] == i:
                    str = str + 'Q|'
                else: str = str + '-|'
            ans.append(str)
        return '\n'.join(ans)

    def __hash__(self):
        return hash(str(self.pos))
    def __str__(self):
        return self.__getAsciiString()
        # return str(self.pos)

# TODO: Implement The methods in this class

class EightQueenSearchProblem(search.SearchProblem):
    """
      Implementation of a Search Problem for the  Eight Queen domain

      Each state is represented by an instance of an eightQueen.
    """
    def __init__(self, puzzle):
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
    puzzle = EightQueenState()
    problem = EightQueenSearchProblem(puzzle)
    path = search.depthFirstSearch(problem)
    print(path)
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))
    curr = puzzle
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)
        input("Press return for the next state...")   # wait for key stroke
        i += 1
