"""
SAT Solver - DIMACS-like Multi-instance Format
----------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <k> <status?>
p cnf <n_vertices> <n_edges>
u,v
x,y
...

Example:
c 1 3 ?
p cnf 4 5
1,2
1,3
2,3
2,4
3,4
c 2 2 ?
p cnf 3 3
1,2
2,3
1,3

OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution


EXAMPLE OUTPUT
------------
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution
3,4,10,U,0.00024808302987366915,BruteForce,{}
4,4,10,S,0.00013304100139066577,BruteForce,"{1: True, 2: False, 3: False, 4: False}"
"""

from typing import List, Tuple, Dict
from src.helpers.sat_solver_helper import SatSolverAbstractClass
import itertools


class SatSolver(SatSolverAbstractClass):

    """
        NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
        For this you dont need to save anything just make sure to return exact related output.
        
        For ease look at the Abstract Solver class and basically we are having the run method which does the saving
        of the CSV file just focus on the logic
    """
    def is_valid(self, clauses:List[List[int]], assignment:Dict[int, bool]) -> bool:
        """
        This definition returns True or False to whether or not the assignment passes all of the clauses
        """
        # check if the curent assigment passes all the clauses
        for clause in clauses:
            # for each clause, check that for each variable in the clause, ONE of the assignments is right (0 or 1)
            found_valid = False
            for var in range(len(clause)): # var is 0 or 1
                #print("clause: " + str(clause) + "VAR: " + str(var))
                if not abs(clause[var]) in assignment : # not assigned a value yet
                    found_valid = True 
                    break
                if assignment[abs(clause[var])] == (clause[var] > 0): # check that, if the first variable is true, the assinment has it as true or if the first variable is false, the assignment has it as false
                    found_valid = True 
                    break # check the next clause                     

            if found_valid == 0: # check if the assignment does not pass this clause
                return False
        return True
    
    def backtack(self, depth, n_vars:int, assignment:Dict[int, bool], clauses:List[List[int]]) -> Dict[int, bool]:
        # if the assignment is of length n_vars, and the depth is beyond that value, return it
        if depth > n_vars:
            return assignment 
        
        # given a new depth, check if either 0 or 1 is valid
        assignment[depth] = 0
        if self.is_valid(clauses, assignment):
            # if 0 at this depth is valid, create a copy of the assignment to run backtrack on (this would be a complete assigment of {} after all the recursive calls)
            new_assignment = assignment.copy()
            new_assignment = self.backtack(depth+1, n_vars, new_assignment, clauses)
            if new_assignment != {}:
                return new_assignment 

        assignment[depth] = 1
        if self.is_valid(clauses, assignment):
            new_assignment = assignment.copy()
            new_assignment = self.backtack(depth+1, n_vars, new_assignment, clauses)
            if new_assignment != {}:
                return new_assignment 

        # depth can = n_vars here; this triggers backtacking
        return dict()
        
    

    def sat_backtracking(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        # clauses [[-2, 3], [-1, 4], [-2, 4], [-4, -2], [-4, -1], [1, 1], [4, 4], [-4, -3], [-1, -4], [3, 3]]
        # Create a Dictionary called assignment that keeps track of the assignments 0/1
        assignment = dict()
        # call on the backtack function to assign a value to x1 which is depth 1
        assignment = self.backtack(1, n_vars, assignment, clauses)
        
        # Try all combinations of assignments using backtracking
        return (assignment != {}, assignment)
    
    def brute_force(self, depth, n_vars:int, assignment:Dict[int, bool], clauses:List[List[int]]) -> Dict[int, bool]:
        for i in range(2): # try both 0 and 1 in 
            # if we are not on the last depth, call on this function
            assignment[depth] = i
            if self.is_valid(clauses, assignment):
                return assignment
            elif depth != n_vars:
                new_assignment = self.brute_force(depth+1, n_vars, assignment, clauses)
                if new_assignment != {}:
                    return new_assignment

        return {}



    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        # Create a Dictionary called assignment that starts off with all keys pointing to being 0; it tracks of the assignments 0/1
        # each clause will ALWAYS be in the assignment
        assignment = self.brute_force(1, n_vars, {(i+1):0 for i in range(n_vars)}, clauses)

        return (assignment != {}, assignment)

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass