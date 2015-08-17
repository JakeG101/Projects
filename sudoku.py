###########################################################################
# sudoku.py
# Part of Artificial Intelligence CSP Project
#
# Authors: Erik Talvitie, Franklin and Marshall College
#          Steele Schauer, Franklin and Marshall College
#
# Last edit: 2/5/15
#
# Defines the Sudoku CSP.
# When run from the command line, generates a Sudoku CSP,
# uses a CSP solver to solve it, verifies the solution,
# and prints the solution to the terminal.
#
# YOU MUST FILL IN THIS FILE!
###########################################################################

import sys
from sudokuPuzzle import *
from cspSolver import *

def getBox(spot): #spot is a tuple
    x = spot[0]
    y = spot[1]
    spotList = []
    if x >= 0 and x < 3:
        if y>= 0 and y < 3:
            for i in range(0, 3):
                for j in range(0, 3):
                    spotList.append((i, j))
        elif y >= 3 and y < 6:
            for i in range(0, 3):
                for j in range(3, 6):
                    spotList.append((i, j))
        elif y >= 6 and y < 9:
            for i in range(0, 3):
                for j in range(6, 9):
                    spotList.append((i, j))
    elif x >= 3 and x < 6:
        if y>= 0 and y < 3:
            for i in range(3, 6):
                for j in range(0, 3):
                    spotList.append((i, j))
        elif y >= 3 and y < 6:
            for i in range(3, 6):
                for j in range(3, 6):
                    spotList.append((i, j))
        elif y >= 6 and y < 9:
            for i in range(3, 6):
                for j in range(6, 9):
                    spotList.append((i, j))
    elif x >= 6 and x < 9:
        if y>= 0 and y < 3:
            for i in range(6, 9):
                for j in range(0, 3):
                    spotList.append((i, j))
        elif y >= 3 and y < 6:
            for i in range(6, 9):
                for j in range(3, 6):
                    spotList.append((i, j))
        elif y >= 6 and y < 9:
            for i in range(6, 9):
                for j in range(6, 9):
                    spotList.append((i, j))    
    #print(spot)
    #print(spotList)
    spotList.remove(spot)
    return spotList

    

def getConstraints():
    """Generates the constraints for the Sudoku CSP."""
    constraints = []
    #YOU MUST FILL IN THIS FUNCTION
    #Generate the binary constraints between squares in a 9x9 Sudoku grid.
    #Note: For the sake of the arc-consistency algorithm, there should
    #      be two constraints for every pair of variables x, y. One
    #      that represents the arc x -> y and one that represents the
    #      arc y -> x.
    #See nQueens.py for a simple example.

    for row in range (9):
        
        for col in range (9):
            """loops through all squares in board"""
            spot1 = (row, col)
            spotList = getBox(spot1) #gets other squares in same box
            for spot2 in spotList: #constrains in same box
                constraints.append(SudokuConstraint(spot1, spot2))
            for i in range(0, 9): #constraints in row and col
                spot2 = (row, i)
                newConstraint = SudokuConstraint(spot1, spot2)
                if newConstraint not in constraints and spot1 != spot2:
                    constraints.append(newConstraint)
                spot2 = (i, col)
                newConstraint = SudokuConstraint(spot1, spot2)
                if newConstraint not in constraints and spot1 != spot2:
                    constraints.append(newConstraint)

    return constraints


def createSudokuCSP(puzzle):
    """Generates the domains and constraints for the Sudoku CSP
    problem and returns a CSP object."""

    #Generate the domains
    #Notes:
    # - Variables are tuples: (row, column)
    # - Values are characters: 1-9 and . (which marks a blank square)
    domains = {}
    for r in range(9):
        for c in range(9):
            if puzzle.getValue(r, c) == '.':
                domains[(r, c)] = list('123456789')
            else:
                domains[(r, c)] = [puzzle.getValue(r, c)]

    #Generate the constraints
    #You must fill in the getConstraints function for this to work!
    constraints = getConstraints()

    return CSP(domains, constraints)

def solveSudoku(puzzle, solver):
    """Creates a Sudoku CSP object from the given puzzle and uses the
    given CSP solver to solve it. Then uses the resulting solution to
    fill in the puzzle. Returns true if the solver provided a solution
    and false if the solver did not (the puzzle is unsolvable)."""
    csp = createSudokuCSP(puzzle)
    assignment = solver.solve(csp)
    
    if assignment != None:
        for r in range(9):
            for c in range(9):
                if puzzle.getValue(r, c) == '.' and assignment[(r, c)] != None:
                    puzzle.setValue(r, c, assignment[(r, c)])
        return True
    else:
        return False

def main():
    """Usage: python sudoku.py <puzzle> [backtrack | local].  
    - puzzle should be the filename of a Sudoku puzzle. 
    - If the second argument is omitted or is "backtrack" a
      backtracking DFS solver is used. If it is "local" a
      hill-climbing CSP solver is used."""

    if len(sys.argv) < 2:
        print("Usage: python sudoku.py <puzzle> [backtrack | local]")
        quit()

    if len(sys.argv) <= 2 or sys.argv[2] == "backtrack":
        solver = CSPSolver()
    elif sys.argv[2] == "local":
        solver = CSPLocalSearch()
    else:
        print("Usage: python sudoku.py <puzzle> [backtrack | local]")
        quit()      

    s = SudokuPuzzle(sys.argv[1])
    print(sys.argv[1])
    s.printPuzzle()

    solvable = solveSudoku(s, solver)
    if not solvable:
        print("Puzzle has no solutions")
    
    print("Solved: " + str(s.isSolved()))
    s.printPuzzle()

if __name__ == '__main__':
    main()
