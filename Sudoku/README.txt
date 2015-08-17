8/17/2015
This was a project I did for Artificial Intelligence. 
The base Sudoku Game code was created by Erik Talvite.

Contains two ways to solve a given Sudoku puzzle. 

Either solved as a constraint problem using arc consistency and backtracking-search. 

E.x
$python sudoku.py puzzles/<.sud file goes here> backtrack

Or solved as a local-search problem that utilizes different techniques including:
-initalizes arc consistency as much as possible
-fills in the remaining numbers randomly, maintaing each small box with 1-9
-counts the # of conflicts and swaps two numbers to have less than or equal to # of conflicts
-performs swaps efficently without adding much processing time
-if 15 swaps occur and the # of conflicts remain the same, restart the search from a new point (this deals with local maxima/minima where the search will get stuck)
-Will always eventually find the global maxima of 0 conflicts (a solved board)

E.x
$python sudokuLocalSearch.py puzzles/<.sud file goes here> <# of attempts>


Will generally solve a difficult sudoku puzzle in less than 30 seconds
