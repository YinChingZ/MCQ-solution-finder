#!/usr/bin/env python3
"""
Main module for the MCQ-solution-finder program.

This program allows users to:
  - Input the number of questions.
  - Input the number of options per question.
  - Add solution attempts with a score.
  - Find possible solutions based on the accumulated attempts.
  - Get a recommendation for the next optimal solution to test (new feature).
"""

import sys
from mcq_solver import MCQSolver
from recommendation import get_recommended_solution

def option_to_int(option_char):
    """Convert option letter (A, B, C, D, etc.) or digit to integer."""
    if option_char.isdigit():
        return int(option_char)
    else:
        return ord(option_char.upper()) - ord('A') + 1

def int_to_option(option_int):
    """Convert an integer (1, 2, 3, 4, ...) to an option letter (A, B, C, D, ...) if possible."""
    # If option_int is within 1-26, map to letters.
    if 1 <= option_int <= 26:
        return chr(ord('A') + option_int - 1)
    else:
        return str(option_int)

def display_menu():
    print("\nMenu:")
    print("1. Add a solution attempt with score")
    print("2. Find possible solutions")
    print("3. Recommend optimal solution (narrow possibilities)")
    print("4. Exit")

def add_solution_attempt(solver, num_questions):
    print("\nEnter your solution attempt (e.g., 'ABCD' or '1234'):")
    solution_input = input().strip()
    if len(solution_input) != num_questions:
        print(f"Error: Solution must have exactly {num_questions} answers.")
        return
    
    solution = [option_to_int(opt) for opt in solution_input]
    try:
        score = int(input("Enter the score (number of correct answers): "))
    except ValueError:
        print("Error: Score must be an integer.")
        return
    
    if score < 0 or score > num_questions:
        print(f"Error: Score must be between 0 and {num_questions}.")
        return
    
    solver.add_solution_with_score(solution, score)
    print("Solution attempt added successfully!")

def find_possible_solutions(solver, options_per_question):
    unique_solution, possible_answers, num_consistent = solver.get_solution()
    print(f"\nFound {num_consistent} consistent solution(s).")
    
    if unique_solution:
        print("\nUnique solution found:")
        formatted_solution = ''.join([
            int_to_option(opt) if (isinstance(options_per_question, int) or (isinstance(options_per_question, list) and options_per_question[i] <= 26))
            else str(opt) for i, opt in enumerate(unique_solution)
        ])
        print(formatted_solution)
    else:
        print("\nPossible answers for each question:")
        for i, options in enumerate(possible_answers):
            options_list = sorted(list(options))
            options_str = ', '.join([
                int_to_option(opt) if (isinstance(options_per_question, int) or (isinstance(options_per_question, list) and options_per_question[i] <= 26))
                else str(opt) for opt in options_list
            ])
            print(f"Q{i+1}: {options_str}")
        
        uncertain = solver.get_uncertain_questions(possible_answers)
        print(f"\nQuestions with uncertainty: {len(uncertain)} ({', '.join(str(q+1) for q in uncertain)})")
        
        # If there are many possibilities, suggest a candidate.
        if num_consistent > 10:
            print("\nSuggested solution to check next (to narrow down possibilities):")
            # Use the current possible solutions to suggest an optimal candidate.
            candidate = get_recommended_solution(solver.get_all_possible_solutions())
            # Format the candidate for display.
            formatted_candidate = ''.join([
                int_to_option(opt) if (isinstance(options_per_question, int) or (isinstance(options_per_question, list) and options_per_question[i] <= 26))
                else str(opt) for i, opt in enumerate(candidate)
            ])
            print(formatted_candidate)

def recommend_solution(solver, options_per_question):
    all_possible = solver.get_all_possible_solutions()
    if not all_possible:
        print("No possible solutions to recommend.")
        return

    recommended = get_recommended_solution(all_possible)
    print("\nRecommended solution set to test next (expected to eliminate the most possibilities):")
    formatted_recommendation = ''.join([
        int_to_option(opt) if (isinstance(options_per_question, int) or (isinstance(options_per_question, list) and options_per_question[i] <= 26))
        else str(opt) for i, opt in enumerate(recommended)
    ])
    print(formatted_recommendation)

def main():
    print("=== Multiple Choice Question Solution Finder ===")
    
    # Get number of questions from user.
    try:
        num_questions = int(input("Enter number of questions: "))
    except ValueError:
        print("Error: Number of questions must be an integer.")
        return
    
    # Get number of options per question.
    options_input = input("Enter number of options per question (e.g., '4' for all ABCD or '4,5,4' for different counts): ")
    if ',' in options_input:
        try:
            options_per_question = [int(x.strip()) for x in options_input.split(',')]
        except ValueError:
            print("Error: Please enter valid integers separated by commas.")
            return
        
        if len(options_per_question) != num_questions:
            print(f"Error: You specified {len(options_per_question)} option counts but have {num_questions} questions.")
            return
    else:
        try:
            options_per_question = int(options_input)
        except ValueError:
            print("Error: Number of options must be an integer.")
            return
    
    # Initialize the MCQ solver.
    solver = MCQSolver(num_questions, options_per_question)
    
    while True:
        display_menu()
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == '1':
            add_solution_attempt(solver, num_questions)
        elif choice == '2':
            find_possible_solutions(solver, options_per_question)
        elif choice == '3':
            recommend_solution(solver, options_per_question)
        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()