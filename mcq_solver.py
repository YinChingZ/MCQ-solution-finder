from typing import List, Set, Tuple, Dict, Optional
import random
from collections import defaultdict
import time

class MCQSolver:
    def __init__(self, num_questions: int, options_per_question: List[int] = None):
        """
        Initialize the MCQ solver.
        
        Args:
            num_questions: Number of questions in the quiz
            options_per_question: List containing number of options for each question
                                 (if single int, all questions have same number of options)
        """
        self.num_questions = num_questions
        
        # If options_per_question is not provided or is an int, convert to list
        if options_per_question is None:
            # Default to 4 options (A, B, C, D) for all questions
            self.options_per_question = [4] * num_questions
        elif isinstance(options_per_question, int):
            self.options_per_question = [options_per_question] * num_questions
        else:
            self.options_per_question = options_per_question
            
        self.solutions_with_scores = []
        self.max_solutions_to_store = 1000  # Limit for performance
        
    def add_solution_with_score(self, solution: List[int], score: int):
        """Add a solution attempt and its corresponding score."""
        self.solutions_with_scores.append((solution, score))
        
    def get_solution(self) -> Tuple[Optional[List[int]], List[Set[int]], int]:
        """
        Find all possible solutions consistent with provided scores.
        
        Returns:
            Tuple containing:
            - Unique solution if one exists, or suggested solution to check next, or None
            - List of sets of possible answers for each question
            - Number of consistent solutions found
        """
        start_time = time.time()
        consistent_solutions = []
        
        def backtrack(partial_solution, index):
            # Stop exploring if we've found too many solutions (for performance)
            if len(consistent_solutions) >= self.max_solutions_to_store:
                return
            
            # If we've assigned all questions, check if the solution is consistent
            if index == self.num_questions:
                if self._is_solution_consistent(partial_solution):
                    consistent_solutions.append(partial_solution[:])
                return
            
            # Try each option for the current question
            for opt in range(1, self.options_per_question[index] + 1):
                partial_solution[index] = opt
                
                # Early pruning: check if partial solution is still viable
                if self._is_partial_solution_consistent(partial_solution, index):
                    backtrack(partial_solution, index + 1)
        
        # Start backtracking
        backtrack([0] * self.num_questions, 0)
        
        # Extract possible answers for each question
        possible_answers = [set() for _ in range(self.num_questions)]
        for sol in consistent_solutions:
            for q, a in enumerate(sol):
                possible_answers[q].add(a)
        
        # Determine what to return based on number of solutions
        if len(consistent_solutions) == 1:
            # Unique solution found
            return consistent_solutions[0], possible_answers, 1
        elif len(consistent_solutions) <= 10:
            # Small set of possible solutions
            return None, possible_answers, len(consistent_solutions)
        else:
            # Too many solutions, suggest one to check next
            suggested = self._suggest_solution_to_check(consistent_solutions)
            return suggested, possible_answers, len(consistent_solutions)
    
    def _is_solution_consistent(self, solution: List[int]) -> bool:
        """Check if a solution is consistent with all recorded solution-score pairs."""
        for test_sol, score in self.solutions_with_scores:
            matches = sum(a == b for a, b in zip(solution, test_sol))
            if matches != score:
                return False
        return True
    
    def _is_partial_solution_consistent(self, partial_solution: List[int], index: int) -> bool:
        """
        Check if a partial solution can potentially be consistent.
        Uses early pruning to avoid exploring impossible branches.
        """
        for test_sol, score in self.solutions_with_scores:
            # Count matches up to the current index
            matches_so_far = sum(a == b for a, b in zip(partial_solution[:index+1], test_sol[:index+1]))
            
            # If matches already exceed score, inconsistent
            if matches_so_far > score:
                return False
            
            # If remaining questions aren't enough to reach score, inconsistent
            remaining_questions = self.num_questions - (index + 1)
            if matches_so_far + remaining_questions < score:
                return False
        
        return True
    
    def _suggest_solution_to_check(self, consistent_solutions: List[List[int]]) -> List[int]:
        """
        Suggest a solution to check that would narrow down possibilities the most.
        Uses information theory principles to maximize information gain.
        """
        suggested = []
        for q in range(self.num_questions):
            # Count frequency of each option
            option_counts = defaultdict(int)
            for sol in consistent_solutions:
                option_counts[sol[q]] += 1
            
            # Choose option closest to half of total solutions (maximizes information gain)
            target = len(consistent_solutions) / 2
            best_option = min(option_counts.keys(), key=lambda opt: abs(option_counts[opt] - target))
            suggested.append(best_option)
        
        return suggested

    def print_possible_answers(self, possible_answers: List[Set[int]]):
        """Print the possible answers for each question in a readable format."""
        for i, options in enumerate(possible_answers):
            options_list = sorted(list(options))
            options_str = ', '.join([str(opt) for opt in options_list])
            print(f"Q{i+1}: {options_str}")
            
    def get_uncertain_questions(self, possible_answers: List[Set[int]]) -> List[int]:
        """Return indices of questions with multiple possible answers."""
        return [i for i, options in enumerate(possible_answers) if len(options) > 1]