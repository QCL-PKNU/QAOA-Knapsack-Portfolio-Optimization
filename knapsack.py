"""Definitions related to the knapsack problem."""
from dataclasses import dataclass, field
import numpy as np


@dataclass
class KnapsackProblem:
    values: list
    weights: list
    max_weight: int
        
    def __post_init__(self):
        self.total_weight = sum(self.weights)
        self.N = len(self.weights)


def value(choice, problem):
    """Return the value of an item choice.
    
    Assumes choice is a numpy array of length problem.N"""
    return choice.dot(problem.values)


def weight(choice, problem):
    """Return the weight of an item choice.
    
    Assumes choice is a numpy array of length problem.N"""
    return choice.dot(problem.weights)


def is_choice_feasible(choice, problem):
    return weight(choice, problem) <= problem.max_weight


def classical_solutions(problem: KnapsackProblem):
    def choices_from_number(problem, number):
        return np.array(list(map(int, list(reversed(bin(number)[2:])))) + [0] * (problem.N - len(bin(number)[2:])))
    best = 0
    solutions = []
    for i in range(2**problem.N):
        choice = choices_from_number(problem, i)
        value = choice.dot(problem.values)
        weight = choice.dot(problem.weights)
        is_legal = weight <= problem.max_weight
        if is_legal and value > best:
            best = value
            solutions = [choice]
        elif is_legal and value == best:
            solutions.append(choice)
    return np.array(solutions)