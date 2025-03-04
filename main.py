from mcq_solver import MCQSolver
import datetime

def option_to_int(option_char):
    """Convert option letter (A, B, C, D) to integer (1, 2, 3, 4)"""
    if option_char.isdigit():
        return int(option_char)
    else:
        return ord(option_char.upper()) - ord('A') + 1

def int_to_option(option_int, max_options=None):
    """Convert integer (1, 2, 3, 4) to option letter (A, B, C, D) or number if > 26"""
    if max_options is not None and max_options > 26:
        return str(option_int)
    else:
        return chr(ord('A') + option_int - 1)

def main():
    # Display header with version info, current date and user
    print("=== Multiple Choice Question Solution Finder ===")
    print("Version: 2.0 (Enhanced Elimination Strategy)")
    print("Date: 2025-03-04 04:43:48 UTC")
    print("User: YinChingZ")
    print("===============================================")
    
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
        print("3. Get optimal solution to check next")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")
        
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
            result = solver.get_solution()
            
            print(f"\nFound {result['num_consistent']} consistent solution(s).")
            
            if result['unique_solution']:
                print("\nUnique solution found:")
                formatted_solution = ''.join([
                    int_to_option(opt, 
                        options_per_question[i] if isinstance(options_per_question, list) 
                        else options_per_question) 
                    for i, opt in enumerate(result['unique_solution'])
                ])
                print(formatted_solution)
            else:
                print("\nPossible answers for each question:")
                for i, options in enumerate(result['possible_answers']):
                    options_list = sorted(list(options))
                    max_opt = (isinstance(options_per_question, list) and options_per_question[i]) or options_per_question
                    options_str = ', '.join([int_to_option(opt, max_opt) for opt in options_list])
                    print(f"Q{i+1}: {options_str}")
                
                uncertain = solver.get_uncertain_questions(result['possible_answers'])
                print(f"\nQuestions with uncertainty: {len(uncertain)} " +
                      f"({', '.join([str(q+1) for q in uncertain])})")
        
        elif choice == '3':
            result = solver.get_solution()
            
            if result['num_consistent'] <= 1:
                if result['num_consistent'] == 1:
                    print("\nUnique solution already found!")
                    formatted_solution = ''.join([
                        int_to_option(opt, 
                            options_per_question[i] if isinstance(options_per_question, list) 
                            else options_per_question) 
                        for i, opt in enumerate(result['unique_solution'])
                    ])
                    print(formatted_solution)
                else:
                    print("\nNo consistent solutions found with current data.")
            else:
                print("\nOptimal solution to check next:")
                formatted_suggestion = ''.join([
                    int_to_option(opt, 
                        options_per_question[i] if isinstance(options_per_question, list) 
                        else options_per_question) 
                    for i, opt in enumerate(result['suggested_solution'])
                ])
                print(formatted_suggestion)
                
                print(f"\nElimination potential: {result['max_elimination']} out of {result['num_consistent']} " +
                      f"solutions ({result['max_elimination']/result['num_consistent']*100:.1f}% reduction)")
                
                # Display detailed elimination statistics
                if result['num_consistent'] <= 100:
                    elimination_efficiency = solver.get_elimination_efficiency(
                        result['score_distribution'], result['num_consistent'])
                    
                    print("\nScore prediction and elimination efficiency:")
                    print("┌──────────┬────────────────┬─────────────────┐")
                    print("│ If Score │ Solutions Left │ Elimination (%) │")
                    print("├──────────┼────────────────┼─────────────────┤")
                    
                    for score in sorted(elimination_efficiency.keys()):
                        solutions_left = result['num_consistent'] - int(elimination_efficiency[score] * 
                                                                      result['num_consistent'] / 100.0)
                        print(f"│ {score:8d} │ {solutions_left:14d} │ {elimination_efficiency[score]:13.1f}% │")
                    
                    print("└──────────┴────────────────┴─────────────────┘")
        
        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
