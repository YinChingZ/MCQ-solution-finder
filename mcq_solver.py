from typing import List, Set, Tuple, Dict, Optional, Any
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
        
    def get_solution(self):
        """
        Find all possible solutions consistent with provided scores.
        
        Returns:
            Dictionary containing:
            - unique_solution: Unique solution if one exists, otherwise None
            - possible_answers: List of sets of possible answers for each question
            - num_consistent: Number of consistent solutions found
            - suggested_solution: Suggested solution to check next (if applicable)
            - max_elimination: Maximum number of solutions that could be eliminated
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
        
        # Find optimal suggestion if more than one solution exists
        suggested_solution = None
        max_elimination = 0
        score_distribution = None
        
        if len(consistent_solutions) > 1:
            suggestion_result = self._find_optimal_suggestion(consistent_solutions)
            suggested_solution = suggestion_result['suggestion']
            max_elimination = suggestion_result['max_elimination']
            score_distribution = suggestion_result['score_distribution']
        
        # Determine what to return based on number of solutions
        if len(consistent_solutions) == 1:
            # Unique solution found
            unique_solution = consistent_solutions[0]
        else:
            unique_solution = None
            
        return {
            'unique_solution': unique_solution,
            'possible_answers': possible_answers,
            'num_consistent': len(consistent_solutions),
            'suggested_solution': suggested_solution,
            'max_elimination': max_elimination,
            'score_distribution': score_distribution
        }
    
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
    
    def _find_optimal_suggestion(self, consistent_solutions: List[List[int]]) -> Dict[str, Any]:
        """
        Find a solution to check that would maximize elimination of other solutions.
        
        Returns dictionary containing:
            - suggestion: The suggested solution to check
            - max_elimination: Maximum number of solutions that could be eliminated
            - score_distribution: Distribution of scores for the suggested solution
        """
        # For small solution sets, use exhaustive search
        if len(consistent_solutions) <= 100:
            return self._find_optimal_suggestion_exhaustive(consistent_solutions)
        else:
            # For larger sets, use heuristic approach
            return self._find_optimal_suggestion_heuristic(consistent_solutions)
    
    def _find_optimal_suggestion_exhaustive(self, consistent_solutions: List[List[int]]) -> Dict[str, Any]:
        """Use exhaustive search to find optimal suggestion for small solution sets."""
        total_solutions = len(consistent_solutions)
        best_suggestion = None
        max_elimination = -1
        best_score_distribution = None
        
        # Try each solution as a potential suggestion
        for candidate in consistent_solutions:
            # Score distribution if this candidate is tested
            score_distribution = defaultdict(int)
            
            # Evaluate how many solutions would be eliminated with this candidate
            for test_solution in consistent_solutions:
                score = sum(a == b for a, b in zip(candidate, test_solution))
                score_distribution[score] += 1
            
            # Calculate maximum elimination potential
            max_bucket = max(score_distribution.values())
            elimination_potential = total_solutions - max_bucket
            
            if elimination_potential > max_elimination:
                max_elimination = elimination_potential
                best_suggestion = candidate
                best_score_distribution = dict(score_distribution)
        
        return {
            'suggestion': best_suggestion,
            'max_elimination': max_elimination, 
            'score_distribution': best_score_distribution
        }
    
    def _find_optimal_suggestion_heuristic(self, consistent_solutions: List[List[int]]) -> Dict[str, Any]:
        """Use information theory-based heuristic for larger solution sets."""
        suggestion = []
        
        # For each question, choose the option that appears closest to 50% of the time
        for q in range(self.num_questions):
            # Count frequency of each option
            option_counts = defaultdict(int)
            for sol in consistent_solutions:
                option_counts[sol[q]] += 1
            
            # Choose option closest to half of total solutions (maximizes information gain)
            target = len(consistent_solutions) / 2
            best_option = min(option_counts.keys(), key=lambda opt: abs(option_counts[opt] - target))
            suggestion.append(best_option)
        
        # Calculate score distribution for this suggestion
        score_distribution = defaultdict(int)
        for sol in consistent_solutions:
            score = sum(a == b for a, b in zip(suggestion, sol))
            score_distribution[score] += 1
        
        # Calculate elimination potential
        max_bucket = max(score_distribution.values())
        elimination_potential = len(consistent_solutions) - max_bucket
        
        return {
            'suggestion': suggestion,
            'max_elimination': elimination_potential,
            'score_distribution': dict(score_distribution)
        }
    
    def get_uncertain_questions(self, possible_answers: List[Set[int]]) -> List[int]:
        """Return indices of questions with multiple possible answers."""
        return [i for i, options in enumerate(possible_answers) if len(options) > 1]
    
    def get_elimination_efficiency(self, score_distribution: Dict[int, int], total_solutions: int) -> Dict[int, float]:
        """Calculate elimination efficiency for each possible score."""
        elimination_efficiency = {}
        
        for score, count in score_distribution.items():
            efficiency = 100.0 * (total_solutions - count) / total_solutions
            elimination_efficiency[score] = efficiency
        
        return elimination_efficiency
