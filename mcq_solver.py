"""
Module: mcq_solver.py

This module implements the MCQSolver class that tracks and reduces the set of possible solutions
for a Multiple Choice Question (MCQ) based on user attempts and provided scores.

Features:
- Initializes all possible solution combinations based on the number of questions and available options.
- Filters the solution space when a solution attempt with a score is provided.
- Provides methods to retrieve a unique solution (if determined), the possible answers per question, and the number of consistent solutions.
- Determines which questions remain uncertain.
"""

import itertools

class MCQSolver:
    def __init__(self, num_questions, options_per_question):
        """
        Initialize the solver with the given number of questions and options per question.
        
        Args:
            num_questions (int): number of questions.
            options_per_question (int or list): if int, each question has that many options (numbered 1 to that number). 
                                                  If list, each element represents the number of options for that question.
        """
        self.num_questions = num_questions
        self.options_per_question = options_per_question
        
        # Generate all possible solution combinations.
        if isinstance(options_per_question, int):
            # All questions have the same number of options.
            choices = [list(range(1, options_per_question + 1))] * num_questions
        elif isinstance(options_per_question, list):
            # Each question may have a different number of options.
            if len(options_per_question) != num_questions:
                raise ValueError("Length of options_per_question list must equal num_questions.")
            choices = [list(range(1, count + 1)) for count in options_per_question]
        else:
            raise ValueError("options_per_question must be an integer or a list of integers.")

        # Cartesian product of choices for all questions.
        self.possible_solutions = list(itertools.product(*choices))
    
    def add_solution_with_score(self, solution, score):
        """
        Add a solution attempt with its score, and filter the possible solutions accordingly.
        
        Args:
            solution (list): a list representing a solution attempt.
            score (int): the number of answers that match the correct solution.
        """
        def matches(s):
            # Compute the number of matching answers between s and the attempted solution.
            return sum(1 for a, b in zip(s, solution) if a == b) == score
        
        self.possible_solutions = [s for s in self.possible_solutions if matches(s)]
    
    def get_solution(self):
        """
        Get the current solution status.
        
        Returns:
            tuple: (unique_solution, possible_answers, num_consistent)
            - unique_solution: the unique solution if only one possibility remains, otherwise None.
            - possible_answers: a list of sets with possible options for each question.
            - num_consistent: count of remaining possible solutions.
        """
        num_consistent = len(self.possible_solutions)
        
        unique_solution = None
        if num_consistent == 1:
            unique_solution = self.possible_solutions[0]
        
        # Build a list containing sets of possible options for each question.
        possible_answers = []
        for i in range(self.num_questions):
            options = set(solution[i] for solution in self.possible_solutions)
            possible_answers.append(options)
        
        return unique_solution, possible_answers, num_consistent
    
    def get_uncertain_questions(self, possible_answers):
        """
        Returns the indices of questions that have more than one possible answer.
        
        Args:
            possible_answers (list of sets): list containing a set of possible answers for each question.
            
        Returns:
            list: indices (0-indexed) of questions with uncertainty.
        """
        return [i for i, opts in enumerate(possible_answers) if len(opts) > 1]
    
    def get_all_possible_solutions(self):
        """
        Returns the current list of all possible solutions.
        """
        return [list(s) for s in self.possible_solutions]