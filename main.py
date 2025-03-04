#!/usr/bin/env python3
"""
Main module for the MCQ-solution-finder program.

This program allows users to:
  - Input the number of questions.
  - Input the number of options per question.
  - Try solution attempts and get a score.
  - Find possible solution sets.
  - Use a new recommendation feature that suggests the optimal solution
    set that is expected to eliminate the most possible solutions.
"""

import sys
from recommendation import get_recommended_solution

# For demonstration purposes, we'll store a list of possible solutions.
# In a real use case, this list would be generated by the program logic based on user inputs.
possible_solutions = [
    ['A', 'B', 'C', 'D'],
    ['A', 'B', 'D', 'C'],
    ['B', 'B', 'C', 'D'],
    ['B', 'A', 'C', 'D']
]

def display_menu():
    print("\nMCQ-solution-finder Menu:")
    print("1. Add solution attempt (simulate score feedback)")
    print("2. Find possible solutions")
    print("3. Recommend optimal solution (new feature)")
    print("4. Exit")

def add_solution_attempt():
    # In a full implementation, this function would allow the user to enter an attempt
    # and provide a score, then filter the possible_solutions accordingly.
    print("Functionality to add a solution attempt is not yet fully implemented.")

def find_possible_solutions():
    # This function would normally display or update the list of possible solutions.
    print("Current possible solutions:")
    for sol in possible_solutions:
        print(sol)

def recommend_solution():
    # Use the new feature to find the optimal guess from the possible_solutions.
    recommendation = get_recommended_solution(possible_solutions)
    print("Recommended solution set to test next is:")
    print(recommendation)

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            add_solution_attempt()
        elif choice == '2':
            find_possible_solutions()
        elif choice == '3':
            recommend_solution()
        elif choice == '4':
            print("Exiting program.")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()