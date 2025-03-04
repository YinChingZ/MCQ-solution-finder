"""
Module: recommendation.py

This module provides a function to recommend an optimal solution set (guess) that, if tested,
is expected to eliminate the most possible solutions based on the feedback (score).

The algorithm works as follows:
1. For a given candidate guess, simulate its feedback (score) against every possible solution.
2. Group the possible solutions by the score (number of matching answers).
3. The worst-case scenario for the candidate is the largest group size (i.e. the maximum number of solutions remaining).
4. The elimination count is defined as the total number of possibilities minus this maximum group size.
5. The recommended guess is the candidate with the maximum elimination (i.e. the smallest worst-case remaining count).
"""

def compute_score(guess, solution):
    """
    Compute the score between the guess and the actual solution.
    The score is defined as the number of positions that match exactly.
    Assumes both guess and solution are lists of answers of the same length.
    """
    return sum(1 for g, s in zip(guess, solution) if g == s)

def get_recommended_solution(possible_solutions, candidate_set=None):
    """
    Recommends an optimal candidate solution set (guess) from the candidate_set based on the elimination criterion.
    
    Args:
        possible_solutions (list of list): A list of possible solution sets. Each solution set is assumed to be a list.
        candidate_set (list of list, optional): A list of candidate guesses to evaluate.
            If None, use possible_solutions as the candidate set.
    
    Returns:
        list: The recommended candidate solution set.
    """
    if candidate_set is None:
        candidate_set = possible_solutions

    best_candidate = None
    max_elimination = -1

    total = len(possible_solutions)
    for candidate in candidate_set:
        # Partition possible solutions by the score outcome if candidate is used as a guess.
        partition = {}
        for sol in possible_solutions:
            score = compute_score(candidate, sol)
            partition[score] = partition.get(score, 0) + 1

        worst_case_remaining = max(partition.values())
        elimination = total - worst_case_remaining
        if elimination > max_elimination:
            max_elimination = elimination
            best_candidate = candidate

    return best_candidate

if __name__ == "__main__":
    # Example usage:
    possible = [
        ['A', 'B', 'C', 'D'],
        ['A', 'B', 'D', 'C'],
        ['B', 'B', 'C', 'D'],
        ['B', 'A', 'C', 'D']
    ]
    recommended = get_recommended_solution(possible)
    print("Recommended solution set:", recommended)