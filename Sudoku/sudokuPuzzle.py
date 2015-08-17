###########################################################################
# sudokuPuzzle.py
# Part of Artificial Intelligence CSP Project
#
# Author: Erik Talvitie, Franklin and Marshall College
#
# Last edit: 2/10/12
#
# Contains a class for representing a sudoku puzzle (read from a text file)
# Should be compatible with Python 2.6 and above
#
# YOU DO NOT NEED TO EDIT THIS FILE!
###########################################################################

class SudokuPuzzle:
    """This class represents a sudoku puzzle."""
    def __init__(self, filename):
        """Creates the puzzle from a text file. The file should
        represent blanks with . or 0 and filled in squares with digits
        1-9. All other characters are ignored. Note: not robust to
        invalid files (e.g. not enough or too many squares in the
        puzzle)."""

        inFile = open(filename)

        self.__board = ['.']*81
        idx = 0
        for line in inFile:
            for c in line:
                if c == '0':
                    c = '.'
                if c in '.123456789':
                    self.__board[idx] = c
                    idx += 1

    def getValue(self, row, col):
        """Returns the entry at a particular square in the puzzle
        (position given by row and col). Will either be . or a digit
        1-9 (returns a character, not a number)."""
        return self.__board[row*9 + col]

    def setValue(self, row, col, value):
        """Sets the entry at a particular square in the puzzle
        (position given by row and col). For sane results, value
        should probably either be . or a character from 1-9."""
        self.__board[row*9 + col] = value

    def printPuzzle(self):
        """Prints the puzzle to the screen in a pretty way."""
        str = '*' + '-'*11 + '*\n'
        for r in range(9):
            if r > 0 and r % 3 == 0:
                str += '|' + ('-'*3 + '+')*2 + '-'*3 + '|\n'
            for c in range(9):
                if c % 3 == 0:
                    str += '|'
                str += self.__board[r*9 + c]
            str += '|\n'
        str += '*' + '-'*11 + '*\n'
        print(str)

    def isSolved(self):
        """Checks if the puzzle is solved. Returns true if it is,
        false otherwise."""
        rows = []
        cols = []
        squares = []
        for i in range(9):
            rows.append({})
            cols.append({})
            squares.append({})

        for i in range(len(self.__board)):
            if self.__board[i] not in '123456789':
                return False
            else:
                r = i // 9
                if self.__board[i] in rows[r]:
                    print("Conflict in row " + str(r))
                    return False
                else:
                    rows[r][self.__board[i]] = self.__board[i]

                c = i % 9
                if self.__board[i] in cols[c]:
                    print("Conflict in column " + str(c))
                    return False
                else:
                    cols[c][self.__board[i]] = self.__board[i]

                squareIndex = (r//3)*3 + c//3
                if self.__board[i] in squares[squareIndex]:
                    print("Conflict in square " + str(squareIndex))
                    return False
                else:
                    squares[squareIndex][self.__board[i]] = self.__board[i]

        return True
