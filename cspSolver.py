###########################################################################
# cspSolver.py
# Part of Artificial Intelligence CSP Project
#
# Authors: Erik Talvitie, Franklin and Marshall College
#          Jake Kaplan, Steele Schauer, Amy Reyes, Franklin and Marshall College
#
# Last edit: 2/10/12
#
# Defines the CSP class and two CSP Solvers.
#
# YOU MUST FILL IN THIS FILE!
###########################################################################

from abc import *
import time
import random
import queue
import copy
import sys

class BinaryConstraint(object):
    """This abstract class represents a binary constraint (a
    constraint between two variables)."""
    __metaclass__ = ABCMeta
    def __init__(self, var1, var2):
        """Takes the two variables to which this constraint should
        apply."""
        self.__variables = (var1, var2)

    def getVariables(self):
        """Returns the variables to which this constraint applies."""
        return self.__variables

    @abstractmethod
    def isValid(self, val1, val2):
        """Abstract method. Should take a value for var1 and a value
        for var2 (val1 and val2 respectively) and return true if those
        values satisfy this constraint."""
        pass

class SudokuConstraint(BinaryConstraint):
    def __init__(self, var1, var2):
        """Takes the two variables to which this constraint should
        apply."""
        super().__init__(var1, var2)
        self.__variables = (var1, var2)

    def getVariables(self):
        """Returns the variables to which this constraint applies."""
        return self.__variables

    def isValid(self, val1, val2):
        """Abstract method. Should take a value, 1 through 9, and returns true if both are different and have a value 1 through 9."""
        if val1 == None or val2 == None:
            return True
        val1 = int(val1)
        val2 = int(val2)
        if(val1<1 or val1>9):
            return False
        if(val2<1 or val2>9):
            return False
        if(val1 == val2):
            return False
        else:
            return True
    def __eq__(self, other):
        return self.getVariables()==other.getVariables()
        

    def __str__(self):
        return(str(self.getVariables()))

class CSP:
    def __init__(self, domains, constraints):
        """Takes the domains and constraints of the CSP problem.
        - domains should be a dictionary where variables are the keys
          and the values are lists, representing the domain of each
          variable.
        - constraints should be a list of BinaryConstraints. Note that
          there should be two constraints for each pair of constrained
          variables (one representing the arc x -> y, the other
          representing the arc y -> x)"""

        self.__domains = domains
        self.__constraints = {}

        #Construct the constraint graph as an adjacency list
        #for easy access to neighbors
        self.__constraintNeighbors = {}
        for v in self.__domains:
            self.__constraintNeighbors[v] = []
            self.__constraints[v] = {}

        #Construct the constraint graph as an adjacency matrix
        #for easy access to constraints
        for c in constraints:
            vars = c.getVariables()
            self.__constraintNeighbors[vars[0]].append(vars[1])
            self.__constraints[vars[0]][vars[1]] = c

    def getDomain(self, var):
        """Returns a *copy* of the domain for the given variable."""
        return self.__domains[var][:]

    def removeValue(self, var, val):
        """Removes the given value from the domain of the given
        variable (does nothing if the value is not in the domain)."""
        if val in self.__domains[var]:
            self.__domains[var].remove(val)

    def addValue(self, var, val):
        """Adds the given value to the domain of the given variable
        (does nothing if the value is in the domain)."""
        if val not in self.__domains[var]:
            self.__domains[var].append(val)

    def setDomain(self, var, domain):
        """Sets the domain of the given variable to the given domain
        (should be a list of possible values)."""
        if var in self.__domains:
            self.__domains[var] = domain

    def isValid(self, var1, val1, var2, val2):
        """Returns true if the assignment of val1 to var1 and val2 to
        var2 would be consistent with the binary constraint between
        var1 and var2 (or if there is no constraint between var1 and
        var2)."""
        if var2 in self.__constraints[var1]:
            return self.__constraints[var1][var2].isValid(val1, val2)
        else:
            return True

    def getNeighbors(self, var):
        """Returns the neighbors of the given var on the constraint
        graph."""
        return self.__constraintNeighbors[var]

    def getNumVariables(self):
        """Returns the number of variables in the CSP."""
        return len(self.__domains)

    def getVariables(self):
        """Returns a list of the variables in the CSP."""
        return list(self.__domains.keys())

class CSPSolver:
    """This class represents a CSP solver."""
    def __init__(self):
        """Initializes a counter to keep track of how many nodes are
        visited during backtracking search."""
        self.__numNodes = 0

    def preProcess(self, csp, q):
        changeList = []
        while q.empty() == False:
            curArc = q.get()
            reviseData = self.revise(csp, curArc[0], curArc[1])
            if reviseData[0]:
                for changePair in reviseData[1]:
                    changeList.append(changePair)
                if len(csp.getDomain(curArc[0])) == 0:
                    return(False, changeList)
                for spot in csp.getNeighbors(curArc[0]):
                    if spot != curArc[1]:
                        q.put((spot, curArc[0]))
        return (True, changeList)

    def revise(self, csp, spot1, spot2):
        revised = False
        changeList = []
        for value1 in csp.getDomain(spot1):
            for value2 in csp.getDomain(spot2):
                if len(csp.getDomain(spot2)) == 1:
                    if csp.isValid(spot1, value1, spot2, value2) == False:
                        csp.removeValue(spot1, value1)
                        revised = True
                        changeList.append((spot1, value1))
        return (revised, changeList)

    def solve(self, csp):
        """Takes a CSP and returns a satisfying assignment (a
        dictionary mapping variables to values) or None if there is no
        solution"""
        startTime = time.time()
        self.__numNodes = 0

        #FILL IN CODE HERE 
        #Pre-process the CSP to impose arc-consistency.
        q = queue.Queue()
        for var in csp.getVariables():
            for neighbor in csp.getNeighbors(var):
                q.put((var, neighbor))
        self.preProcess(csp, q)
        
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
        #You must fill in __backtrackingSearch for this to work.
        assignment = self.__backtrackingSearch(csp, assignment)
        print("Search took " + str(time.time() - startTime) + "s and visited " + str(self.__numNodes) + " nodes.")
        return assignment

    def __backtrackingSearch(self, csp, assignment):
        """Takes a CSP, and an initial assignment. Performs MAC
        (backtracking DFS while maintaining arc-consistency after each
        eassignment). Either returns a satisfying assignment or None
        if no such assignment exists."""
        if None not in assignment.values():
            #The assignment is complete: return it.
            return assignment
        else:
            #Leave this here (counts how many nodes you expand)
            self.__numNodes += 1
            var = self.getMinVar(csp, assignment)
            #YOU MUST FILL IN THIS FUNCTION 
            valList = self.getLeastConstrained(csp, var)
            #valList = csp.getDomain(var)
            assignChanges = []
            for value in valList:
                v = value[1]
                domainCopy = csp.getDomain(var)[:]
                oldVal = assignment[var]
                assignment[var] = v
                assignChanges.append((var, oldVal))
                csp.setDomain(var, [v])
                q = self.getNeighborQ(csp, var)
                change, changeList = self.preProcess(csp, q)
                if change == True:
                    for i in changeList:
                        if len(csp.getDomain(i[0])) == 1:
                            oldVal = assignment[i[0]]
                            assignment[i[0]] = csp.getDomain(i[0])[0]
                            assignChanges.append((i[0], oldVal))
                    allVars = csp.getVariables()
                    result = self.__backtrackingSearch(csp, assignment)
                    if result != None:
                        return result
                for a in assignChanges:
                    assignment[a[0]] = a[1]
                    assignChanges.remove(a)
                for i in changeList:
                    csp.addValue(i[0], i[1])
                csp.setDomain(var, domainCopy)
            
            return None

    def getNeighborQ(self,csp, var):
        q = queue.Queue()
        neighbors = csp.getNeighbors(var)
        for neighbor in neighbors:
            q.put((neighbor, var))
            
        return q

    def getLeastConstrained(self,csp,var):
        
        domain = csp.getDomain(var)
        copy = domain[:]
        mini = sys.maxsize 
        minVal = None
        valList = []
        for v in copy:

            csp.setDomain(var, [v])
            q = self.getNeighborQ(csp, var)
            changed, changedList = self.preProcess(csp, q)

            mini = len(changedList)
            minVal = (mini, v)
            valList.append(minVal)
            for changes in changedList:
                csp.addValue(changes[0], changes[1])
            
        csp.setDomain(var, copy)
        valList.sort()
        
        return valList
        

    def getMinVar(self, csp, assignment):
        keys = []
        for var in csp.getVariables():
            if len(csp.getDomain(var)) > 1:
                keys.append(var)
        minVar = keys[0]
        minLen = len(csp.getDomain(keys[0]))
        
        for key in keys:
            if len(csp.getDomain(key))==minLen:
                count1 = 0 
                for neighbor in csp.getNeighbors(key):
                    if len(csp.getDomain(neighbor)) > 1:
                        count1 = count1 + 1
                count2 = 0
                for neighbor in csp.getNeighbors(minVar):
                    if len(csp.getDomain(neighbor)) > 1:
                        count2 = count2 + 1
                if count1 > count2:
                    minVar = key
                    minLen = len(csp.getDomain(key))
            elif len(csp.getDomain(key))<minLen:
                minVar = key
                minLen = len(csp.getDomain(key))
        return minVar
                
        
        
class CSPLocalSearch(CSPSolver):
    """A subclass of CSPSolver that uses steepest-ascent hill-climbing
    instead of backtracking search to solve the given CSP."""
    def solve(self, csp):
        """Takes a CSP and returns an assignment (may or may not be a
        satisfying assignment)."""
        #For reporting the run-time of the search
        startTime = time.time()
        #Should count the number of steps your search takes
        #(You will want to update this counter in your code)
        numSteps = 0
        #Generate a random assignment
        assignment = {}
        for x in csp.getVariables():
            assignment[x] = random.choice(csp.getDomain(x))
        #YOU MUST FILL IN THIS FUNCTION
        #Perform steepest-ascent hill-climbing using the min-conflicts
        #objective function and return the local optimum you
        #reach. You should allow a limited number of sideways steps.
        numSideSteps = 0
        end = False
        while not end:
            conflict = {}
            mini = len(csp.getVariables())+1
            minVar = None
            for var in csp.getVariables(): #MAKES DICT OF CONFLICTS
                x = self.getNumConflicts(var, csp, assignment)
                if x != 0:
                    conflict[var] = x
                    if x < mini:
                        mini = x
                        minVar = var
            if minVar == None:
                end = True
            else:
                minVar = random.choice(list(conflict.keys()))
                domains = csp.getDomain(minVar)
                oldVal = assignment[minVar]
                conflict2 = {}
                mini2 = len(csp.getVariables())+1
                minVal = None
                for val in domains:
                    if val != oldVal:
                        assignment[minVar] = val #sets new value
                        numConflict = self.getNumConflicts(minVar, csp, assignment)
                        conflict2[val] = numConflict
                        if numConflict < mini2:
                            mini2 = numConflict
                            minVal = val
                if mini2 == conflict[minVar]:
                    numSideSteps+=1
                    assignment[minVar] = minVal #NOT SURE IF STEPS OR NOT
                    if numSideSteps >= 1000:
                        end = True
                else:
                    numSideSteps = 0
                    assignment[minVar] = minVal
            numSteps+=1
        
        
        runtime = time.time() - startTime
        print("Local search took " + str(runtime) + "s and " + str(numSteps) + " steps. (" + str(float(runtime)/numSteps) + "s per step.)")
        return assignment


    def getNumConflicts(self, j, csp, assignment):
        numConflicts = 0
        for i in csp.getNeighbors(j):
            if i != j:
                val1 = assignment[i]
                val2 = assignment[j]
                if csp.isValid(i, val1, j, val2) == False:
                            numConflicts+=1
        return numConflicts
    """def getNumConflicts(self, j, csp, assignment):
        n = len(csp.getVariables())
        numConflicts = 0
        for i in range(n):
            if i != j:
                dist = abs(i - j)
                if assignment[i] == assignment[j] + dist or assignment[i] == assignment[j] - dist or assignment[i] == assignment[j]:
                        numConflicts+=1
        return numConflicts"""
