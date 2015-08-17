###########################################################################
# sudokuLocalSearch.py
# Part of Artificial Intelligence CSP Project
#
# Authors: Erik Talvitie, Franklin and Marshall College
#          YOUR NAME HERE, Franklin and Marshall College
#
# Last edit: 2/5/15
#
# When run from the command line takes a sudoku puzzle
# and solves it using local search. Performs the search
# a number of times and reports the average run-time.
#
# YOU MUST FILL IN THIS FILE!
###########################################################################

import sys
from sudoku import *
from sudokuPuzzle import *
from cspSolver import *
import random
import math
import copy

def getRowConflicts(row, col, puzzle, newVal = -1):
    conflicts = {'1': -1, '2': -1,'3': -1, '4': -1,'5': -1, '6': -1,'7': -1, '8': -1, '9': -1}
    for i in range(9):
        val = puzzle.getValue(row, i)
        conflicts[val] = conflicts[val]+1
    if newVal != -1:
        oldVal = puzzle.getValue(row, col)
        conflicts[oldVal] = conflicts[oldVal] - 1
        conflicts[newVal] = conflicts[newVal] + 1
    total = 0
    for key in conflicts.keys():
        if conflicts[key] > 0:
            total = total + conflicts[key]
    return total

def getColConflicts(row, col, puzzle, newVal = -1):
    conflicts = {'1': -1, '2': -1,'3': -1, '4': -1,'5': -1, '6': -1,'7': -1, '8': -1, '9': -1}
    for i in range(9):
        val = puzzle.getValue (i, col)
        conflicts[val] = conflicts[val]+1
    if newVal != -1:
        oldVal = puzzle.getValue(row, col)
        conflicts[oldVal] = conflicts[oldVal] - 1
        conflicts[newVal] = conflicts[newVal] + 1
    total = 0
    for key in conflicts.keys():
        if conflicts[key] > 0:
            total = total + conflicts[key]
    return total

def getConflicts(row, col, puzzle, newVal = -1):
    conflicts = {'1': -1, '2': -1,'3': -1, '4': -1,'5': -1, '6': -1,'7': -1, '8': -1, '9': -1}
    conflicts2 = {'1': -1, '2': -1,'3': -1, '4': -1,'5': -1, '6': -1,'7': -1, '8': -1, '9': -1}
    for i in range(9):
        val = puzzle.getValue(row, i)
        val2 = puzzle.getValue(i, col)
        conflicts[val] = conflicts[val]+1
        conflicts2[val2] = conflicts2[val2]+1
    if newVal != -1:
        oldVal = puzzle.getValue(row, col)
        conflicts[oldVal] = conflicts[oldVal] - 1
        conflicts[newVal] = conflicts[newVal] + 1
        conflicts2[oldVal] = conflicts2[oldVal] - 1
        conflicts2[newVal] = conflicts2[newVal] + 1
    total = 0
    for key in conflicts.keys():
        if conflicts[key] > 0:
            total = total + conflicts[key]
        if conflicts2[key] > 0:
            total = total + conflicts2[key]
    return total

#DICTIONARY of numbers in a row and times they appear
#subtract number of keys
#gives total num conflicts for 1 row

def randomRestart(puzzle):
      for x in range(0, 9, 3):
        for y in range(0, 9, 3):
            valList = '123456789'
            for x1 in range(x, x+3):
                for y1 in range(y, y+3):
                    val = puzzle.getValue(x1, y1)
                    if val != '.':
                        #givenVars[(x1, y1)] = val
                        valList = valList.replace(val, '')
                        
            for x1 in range(x, x+3):
                for y1 in range(y, y+3):
                    val = puzzle.getValue(x1, y1)
                    if val == '.':
                        randnum = random.randint(0, len(valList)-1)
                        num = valList[randnum]
                        puzzle.setValue(x1, y1, num)
                        valList = valList.replace(num, '')

def solveSudokuLocal(puzzle):
    """Solves the given Sudoku puzzle using local search. When the
    function returns, the puzzle will be filled in with its
    solution."""
    #For reporting the run-time of your search.
    startTime = time.time()
    #For reporting the number of steps your search takes.
    #(You will want to keep this counter updated in your code).
    numMoves = 0

    csp = createSudokuCSP(puzzle)

###########From cspSolver.py - solve but mutated for use##############
    q = queue.Queue()
    for var in csp.getVariables():
        for neighbor in csp.getNeighbors(var):
            q.put((var, neighbor))
    solver = CSPSolver()
    CSPSolver.preProcess(solver, csp, q)
    #Set up the initial assignment
    assignment = {}
    for v in csp.getVariables():
        if len(csp.getDomain(v)) == 0:
            #There is no solution
            return None
        elif len(csp.getDomain(v)) == 1:
            #This variable is fully constrained
            assignment[v] = csp.getDomain(v)[0]
        else:
            #This variable is as yet unassigned
            assignment[v] = None
    for key in assignment.keys():
        if assignment[key] != None:
            puzzle.setValue(key[0], key[1], assignment[key])
    originalPuzzle = copy.deepcopy(puzzle)
    #YOU MUST FILL IN THIS FUNCTION 
    #Create a local-search-based Sudoku solver. At the end, the values
    #in the puzzle should constitute a solution. That is, do not
    #return until you have found a solution. No local optima!
    givenVars = {}
    #INITIAL ASSIGNMENT
    puzzle.printPuzzle()
    for x in range(0, 9, 3):
        for y in range(0, 9, 3):
            valList = '123456789'
            for x1 in range(x, x+3):
                for y1 in range(y, y+3):
                    val = puzzle.getValue(x1, y1)
                    if val != '.':
                        givenVars[(x1, y1)] = val
                        valList = valList.replace(val, '')
                        
            for x1 in range(x, x+3):
                for y1 in range(y, y+3):
                    val = puzzle.getValue(x1, y1)
                    if val == '.':
                        randnum = random.randint(0, len(valList)-1)
                        num = valList[randnum]
                        puzzle.setValue(x1, y1, num)
                        valList = valList.replace(num, '')
    totalConflicts = 0
    count = 0
    givenSpots = givenVars.keys()
    boxes = []
    for i in range(9):
        boxes.append([])
        spots = getBoxCoords(i)
        for x in range(spots[0], spots[0]+3):
            for y in range(spots[1], spots[1]+3):
                if (x, y) not in givenSpots:
                    boxes[-1].append((x, y))
    for i in(boxes):
        if i == []:
            boxes.remove(i)
    boxPairs = []
    for thing in boxes:
        while thing != []:
            curBox = thing[0]
            for y in thing:
                if curBox != y:
                    boxPairs.append((curBox, y))
            thing.pop(0)
    for x in range(9):
        totalConflicts = totalConflicts + getRowConflicts(x, x, puzzle)
        totalConflicts = totalConflicts + getColConflicts(x, x, puzzle)
    #for i in range(9):
        #totalConflicts = totalConflicts + getConflicts(i, i, puzzle)
    if totalConflicts != 0:
        end = False
    else:
        end = True
    tempature = 1000
    count = 0
    smallest = sys.maxsize
    while end == False:
        minimum = totalConflicts+1
        finalSpot1 = None
        finalSpot2 = None
        spot1 = None
        spot2 = None
        counter = 0
        boxPairs2 = boxPairs[:]
        first = True
        while minimum >= totalConflicts and boxPairs2 != []:
            newTotalConflicts = totalConflicts
            idx = random.randint(0, len(boxPairs2)-1)
            spot1 = boxPairs2[idx][0]
            spot2 = boxPairs2[idx][1]
            if spot1[0] == spot2[0]:#IF THEY THE SAME ROW WE DONT CARE
                newTotalConflicts = newTotalConflicts - getColConflicts(spot1[0], spot1[1], puzzle)
                newTotalConflicts = newTotalConflicts - getColConflicts(spot2[0], spot2[1], puzzle)
                newTotalConflicts = newTotalConflicts + getColConflicts(spot1[0], spot1[1], puzzle, puzzle.getValue(spot2[0], spot2[1]))
                newTotalConflicts = newTotalConflicts + getColConflicts(spot2[0], spot2[1], puzzle, puzzle.getValue(spot1[0], spot1[1]))
            elif spot1[1] == spot2[1]: #THEY SAME COL WE ONLY CARE ROW
                newTotalConflicts = newTotalConflicts - getRowConflicts(spot1[0], spot1[1], puzzle)
                newTotalConflicts = newTotalConflicts - getRowConflicts(spot2[0], spot2[1], puzzle)
                newTotalConflicts = newTotalConflicts + getRowConflicts(spot1[0], spot1[1], puzzle, puzzle.getValue(spot2[0], spot2[1]))
                newTotalConflicts = newTotalConflicts + getRowConflicts(spot2[0], spot2[1], puzzle, puzzle.getValue(spot1[0], spot1[1]))
            else:
                newTotalConflicts = newTotalConflicts - getConflicts(spot1[0], spot1[1], puzzle)
                newTotalConflicts = newTotalConflicts - getConflicts(spot2[0], spot2[1], puzzle)
                newTotalConflicts = newTotalConflicts + getConflicts(spot1[0], spot1[1], puzzle, puzzle.getValue(spot2[0], spot2[1]))
                newTotalConflicts = newTotalConflicts + getConflicts(spot2[0], spot2[1], puzzle, puzzle.getValue(spot1[0], spot1[1]))
            if newTotalConflicts < minimum:
                minimum = newTotalConflicts
                finalSpot1 = spot1
                finalSpot2 = spot2
            else:
                boxPairs2.pop(idx)
        if minimum < smallest:
            puzzle.printPuzzle()
            smallest = minimum
            print("SMALLEST", smallest)
        if minimum < totalConflicts:
            count = 0
            spot1 = finalSpot1
            spot2 = finalSpot2
            temp = puzzle.getValue(spot2[0], spot2[1])
            puzzle.setValue(spot2[0], spot2[1], puzzle.getValue(spot1[0], spot1[1]))
            puzzle.setValue(spot1[0], spot1[1], temp)
            totalConflicts = minimum
        elif minimum > totalConflicts or count > 15:
            count = 0
            puzzle = copy.deepcopy(originalPuzzle)
            randomRestart(puzzle)
            totalConflicts = 0
            for x in range(9):
                totalConflicts = totalConflicts + getRowConflicts(x, x, puzzle)
                totalConflicts = totalConflicts + getColConflicts(x, x, puzzle)
        elif minimum == totalConflicts and totalConflicts!= 0:
            count = count + 1
            spot1 = finalSpot1
            spot2 = finalSpot2
            temp = puzzle.getValue(spot2[0], spot2[1])
            puzzle.setValue(spot2[0], spot2[1], puzzle.getValue(spot1[0], spot1[1]))
            puzzle.setValue(spot1[0], spot1[1], temp)
            totalConflicts = minimum
        if totalConflicts == 0:
            end = True  
        numMoves+=1  
    print("Local search took " + str(time.time() - startTime) + " and " + str(numMoves) + " steps.")
    return puzzle

def getBoxCoords(num): 
    return ((num-(num%3)),((num%3)*3))

def main():
    """Usage: python sudoku.py <puzzle> <numTrials>
    - puzzle should be the filename of a Sudoku puzzle. 
    - numTrials is the number of times the search will be
      performed.
    Solves the puzzle numTrials times and reports the average time to
    solution in seconds."""

    if len(sys.argv) < 3:
        print("Usage: python sudokuLocalSearch.py <puzzle> <numTrials>")
        quit()

    s = SudokuPuzzle(sys.argv[1])
    print(sys.argv[1])
    s.printPuzzle()

    numTrials = int(sys.argv[2])
    timeSum = 0
    for i in range(numTrials):
        startTime = time.time()
        s = solveSudokuLocal(s)
        timeSum += time.time() - startTime
        
        print("Solved: " + str(s.isSolved()))
        s = SudokuPuzzle(sys.argv[1])
    print("Average time: " + str(float(timeSum)/numTrials) + "s")

if __name__ == '__main__':
    main()
#TEMP CODE
    """probability = newTotalConflicts-oldTotalConflicts
    if tempature != 0:
    probability = math.e**(-1*probability/tempature)
    else:
    probability = .01
    if random.random() < probability:
    temp = puzzle.getValue(spot2[0], spot2[1])
    puzzle.setValue(spot2[0], spot2[1], puzzle.getValue(spot1[0], spot1[1]))
    puzzle.setValue(spot1[0], spot1[1], temp)
    totalConflicts = newTotalConflicts"""
