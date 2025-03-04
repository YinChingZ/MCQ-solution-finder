from mcq_solver import MCQSolver

def option_to_int(option_char):
    """Convert option letter (A, B, C, D) to integer (1, 2, 3, 4)"""
    if option_char.isdigit():
        return int(option_char)
    else:
        return ord(option_char.upper()) - ord('A') + 1

def int_to_option(option_int):
    """Convert integer (1, 2, 3, 4) to option letter (A, B, C, D)"""
    return chr(ord('A') + option_int - 1)

def main():
    print("=== Multiple Choice Question Solution Finder ===")
    
    # Get number of questions
    num_questions = int(input("Enter number of questions: "))
    
    # Get number of options per question
    options_input = input("Enter number of options per question (e.g., '4' for all ABCD or '4,5,4' for different counts): ")
    if ',' in options_input:
        options_per_question = [int(x.strip()) for x in options_input.split(',')]
        if len(options_per_question) != num_questions:
            print(f"Error: You specified {len(options_per_question)} option counts but have {num_questions} questions.")
            return
    else:
        options_per_question = int(options_input)
    
    # Initialize solver
    solver = MCQSolver(num_questions, options_per_question)
    
    while True:
        print("\nMenu:")
        print("1. Add a solution attempt with score")
        print("2. Find possible solutions")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            print("\nEnter your solution attempt (e.g., 'ABCD' or '1234'):")
            solution_input = input().strip()
            
            if len(solution_input) != num_questions:
                print(f"Error: Solution must have exactly {num_questions} answers.")
                continue
                
            solution = [option_to_int(opt) for opt in solution_input]
            score = int(input("Enter the score (number of correct answers): "))
            
            if score < 0 or score > num_questions:
                print(f"Error: Score must be between 0 and {num_questions}.")
                continue
                
            solver.add_solution_with_score(solution, score)
            print("Solution attempt added successfully!")
            
        elif choice == '2':
            unique_solution, possible_answers, num_consistent = solver.get_solution()
            
            print(f"\nFound {num_consistent} consistent solution(s).")
            
            if unique_solution:
                print("\nUnique solution found:")
                formatted_solution = ''.join([int_to_option(opt) if isinstance(options_per_question, int) or options_per_question[i] <= 26 
                                             else str(opt) for i, opt in enumerate(unique_solution)])
                print(formatted_solution)
            else:
                print("\nPossible answers for each question:")
                for i, options in enumerate(possible_answers):
                    options_list = sorted(list(options))
                    options_str = ', '.join([int_to_option(opt) if isinstance(options_per_question, int) or 
                                           (isinstance(options_per_question, list) and options_per_question[i] <= 26)
                                           else str(opt) for opt in options_list])
                    print(f"Q{i+1}: {options_str}")
                
                uncertain = solver.get_uncertain_questions(possible_answers)
                print(f"\nQuestions with uncertainty: {len(uncertain)} ({', '.join([str(q+1) for q in uncertain])})")
                
                if num_consistent > 10:
                    print("\nSuggested solution to check next (to narrow down possibilities):")
                    suggested = unique_solution  # This will be the suggested solution from get_solution()
                    formatted_suggestion = ''.join([int_to_option(opt) if isinstance(options_per_question, int) or options_per_question[i] <= 26 
                                                 else str(opt) for i, opt in enumerate(suggested)])
                    print(formatted_suggestion)
        
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()