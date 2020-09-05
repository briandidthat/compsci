from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod

V = TypeVar("V")  # define type-var V for variables in csp problem

D = TypeVar("D")  # define type-var D for domains in csp problem


class Constraint(Generic[V, D], ABC):
    """
    Constraint is be the base class for all constraints used in a constraint satisfaction problem.
    """

    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    # must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        pass


class CSP(Generic[V, D]):
    """
    A constraint satisfaction problem consists of Variables of type V that have ranges of values known as
    Domains of type D and constraints that determine whether a particular variables domain selection is valid.
    """

    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables = variables
        self.domains = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Each variable should have a domain assigned to it.")

    # goes through all of the variables touched by a given constraint and adds itself to the constraints mapping
    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not present in CSP.")
            else:
                self.constraints[variable].append(constraint)

    # goes through every constraint for a given variable, and check if the constraints have been satisfied given the
    # new assignment. If thew assignment satisfies all constraints, True is returned.
    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    # recursive depth first search variation to find solution
    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        # assignment is complete if every variable is assigned (base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        # get every possible domain value of the first unassigned variable
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # if we're still consistent, we recurse (continue searching)
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                if result is not None:  # if we didn't find the result, we will end up backtracking
                    return result
        return None
