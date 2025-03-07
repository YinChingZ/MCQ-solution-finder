# MCQ-solution-finder

## Description (English)

MCQ-solution-finder is a Python program designed to help users find possible solutions to multiple choice questions (MCQs) based on their solution attempts and scores. The program allows users to input the number of questions and options per question, add solution attempts with scores, and find possible solutions.

## Description (中文)

MCQ-solution-finder 是一个 Python 程序，旨在帮助用户根据他们的解答尝试和得分找到多项选择题（MCQ）的可能解答。该程序允许用户输入问题数量和每个问题的选项数量，添加带有得分的解答尝试，并找到可能的解答。

## Usage Instructions (English)

1. Clone the repository:
   ```
   git clone https://github.com/YinChingZ/MCQ-solution-finder.git
   cd MCQ-solution-finder
   ```

2. Ensure you have Python installed (version 3.6 or higher).

3. Run the main script:
   ```
   python main.py
   ```

4. Follow the on-screen instructions to interact with the program:
   - Enter the number of questions.
   - Enter the number of options per question (e.g., '4' for all ABCD or '4,5,4' for different counts).
   - Choose from the menu options to add a solution attempt with score, find possible solutions, or exit the program.

## Usage Instructions (中文)


1. 克隆仓库：
   ```
   git clone https://github.com/YinChingZ/MCQ-solution-finder.git
   cd MCQ-solution-finder
   ```


2. 确保您已安装 Python（版本 3.6 或更高）。


4. 运行主脚本：
   ```
   python main.py
   ```


4. 按照屏幕上的说明与程序交互：
   - 输入问题数量。
   - 输入每个问题的选项数量（例如，'4' 表示所有问题都有 ABCD 选项，或 '4,5,4' 表示不同问题有不同数量的选项）。
   - 从菜单选项中选择添加带有得分的解答尝试、查找可能的解答或退出程序。

## Potential Issues and Troubleshooting (English)

### Performance Limitations

The program has a performance limitation due to the maximum number of solutions stored (`max_solutions_to_store` is set to 1000). If the number of consistent solutions exceeds this limit, the program may not be able to find all possible solutions. To address this issue, consider increasing the `max_solutions_to_store` value in `mcq_solver.py` or optimizing the solution-finding algorithm.

### Handling Different Option Counts per Question

The program supports different option counts per question. However, if the input for the number of options per question is not consistent with the number of questions, the program will display an error message. Ensure that the input for the number of options per question matches the number of questions.

### Dependencies

The program does not have any external dependencies. It uses standard Python libraries.

### Troubleshooting Steps


- If you encounter any issues while running the program, ensure that you have the correct version of Python installed.
- Check for any error messages displayed by the program and follow the instructions provided.
- If the program is not behaving as expected, review the input values for the number of questions and options per question to ensure they are correct.

## 潜在问题和故障排除 (中文)

### 性能限制

该程序由于存储的最大解答数量（`max_solutions_to_store` 设置为 1000）而存在性能限制。如果一致解答的数量超过此限制，程序可能无法找到所有可能的解答。为了解决此问题，可以考虑增加 `mcq_solver.py` 中的 `max_solutions_to_store` 值或优化解答查找算法。

### 处理每个问题的不同选项数量

该程序支持每个问题的不同选项数量。但是，如果每个问题的选项数量输入与问题数量不一致，程序将显示错误消息。确保每个问题的选项数量输入与问题数量匹配。

### 依赖关系

该程序没有任何外部依赖。它使用标准的 Python 库。

### 故障排除步骤

- 如果在运行程序时遇到任何问题，请确保已安装正确版本的 Python。
- 检查程序显示的任何错误消息并按照提供的说明进行操作。
- 如果程序未按预期运行，请检查问题数量和每个问题的选项数量的输入值，以确保它们是正确的。

## Explanation of Code (English)

### main.py

The `main.py` file contains the main logic of the program. It includes functions to convert option letters to integers and vice versa, display the program header, get user input, and interact with the `MCQSolver` class to add solution attempts, find possible solutions, and get optimal solutions to check next.

#### Functions

- `option_to_int(option_char)`: Converts an option letter (A, B, C, D) to an integer (1, 2, 3, 4).
- `int_to_option(option_int, max_options=None)`: Converts an integer (1, 2, 3, 4) to an option letter (A, B, C, D) or a number if the integer is greater than 26.
- `main()`: The main function that displays the program header, gets user input, initializes the `MCQSolver`, and provides a menu for the user to interact with the program.

### mcq_solver.py

The `mcq_solver.py` file contains the `MCQSolver` class, which is responsible for managing the solution attempts and scores, finding consistent solutions, and suggesting optimal solutions to check next. The class includes methods to add solution attempts, check solution consistency, and find optimal suggestions using both exhaustive and heuristic approaches.

#### MCQSolver Class

- `__init__(self, num_questions: int, options_per_question: List[int] = None)`: Initializes the MCQ solver with the number of questions and options per question.
- `add_solution_with_score(self, solution: List[int], score: int)`: Adds a solution attempt and its corresponding score.
- `get_solution(self)`: Finds all possible solutions consistent with the provided scores and returns a dictionary containing the unique solution (if one exists), possible answers for each question, the number of consistent solutions, a suggested solution to check next, and the maximum number of solutions that could be eliminated.
- `_is_solution_consistent(self, solution: List[int]) -> bool`: Checks if a solution is consistent with all recorded solution-score pairs.
- `_is_partial_solution_consistent(self, partial_solution: List[int], index: int) -> bool`: Checks if a partial solution can potentially be consistent using early pruning to avoid exploring impossible branches.
- `_find_optimal_suggestion(self, consistent_solutions: List[List[int]]) -> Dict[str, Any]`: Finds a solution to check that would maximize the elimination of other solutions using either exhaustive search or a heuristic approach.
- `_find_optimal_suggestion_exhaustive(self, consistent_solutions: List[List[int]]) -> Dict[str, Any]`: Uses exhaustive search to find the optimal suggestion for small solution sets.
- `_find_optimal_suggestion_heuristic(self, consistent_solutions: List[List[int]]) -> Dict[str, Any]`: Uses an information theory-based heuristic for larger solution sets.
- `get_uncertain_questions(self, possible_answers: List[Set[int]]) -> List[int]`: Returns the indices of questions with multiple possible answers.
- `get_elimination_efficiency(self, score_distribution: Dict[int, int], total_solutions: int) -> Dict[int, float]`: Calculates the elimination efficiency for each possible score.

## 代码解释 (中文)

### main.py

`main.py` 文件包含程序的主要逻辑。它包括将选项字母转换为整数及其反向转换的函数，显示程序头部，获取用户输入，并与 `MCQSolver` 类交互以添加解答尝试、查找可能的解答以及获取下一个要检查的最佳解答。

#### 函数

- `option_to_int(option_char)`: 将选项字母（A、B、C、D）转换为整数（1、2、3、4）。
- `int_to_option(option_int, max_options=None)`: 将整数（1、2、3、4）转换为选项字母（A、B、C、D）或如果整数大于 26 则转换为数字。
- `main()`: 主函数，显示程序头部，获取用户输入，初始化 `MCQSolver`，并提供菜单供用户与程序交互。

### mcq_solver.py

`mcq_solver.py` 文件包含 `MCQSolver` 类，该类负责管理解答尝试和得分，查找一致的解答，并建议下一个要检查的最佳解答。该类包括添加解答尝试、检查解答一致性以及使用穷举和启发式方法查找最佳建议的方法。

#### MCQSolver 类

- `__init__(self, num_questions: int, options_per_question: List[int] = None)`: 初始化 MCQ 解答器，包含问题数量和每个问题的选项数量。
- `add_solution_with_score(self, solution: List[int], score: int)`: 添加解答尝试及其对应的得分。
- `get_solution(self)`: 查找与提供的得分一致的所有可能解答，并返回包含唯一解答（如果存在）、每个问题的可能答案、一致解答的数量、下一个要检查的建议解答以及可以消除的最大解答数量的字典。
- `_is_solution_consistent(self, solution: List[int]) -> bool`: 检查解答是否与所有记录的解答-得分对一致。
- `_is_partial_solution_consistent(self, partial_solution: List[int], index: int) -> bool`: 使用早期修剪检查部分解答是否可能一致，以避免探索不可能的分支。
- `_find_optimal_suggestion(self, consistent_solutions: List[List[int]]) -> Dict[str, Any]`: 查找一个解答，以最大化消除其他解答，使用穷举搜索或启发式方法。
- `_find_optimal_suggestion_exhaustive(self, consistent_solutions: List[List[int]]) -> Dict[str, Any]`: 使用穷举搜索查找小解答集的最佳建议。
- `_find_optimal_suggestion_heuristic(self, consistent_solutions: List[List[int]]) -> Dict[str, Any]`: 使用基于信息理论的启发式方法查找较大解答集的最佳建议。
- `get_uncertain_questions(self, possible_answers: List[Set[int]]) -> List[int]`: 返回具有多个可能答案的问题索引。
- `get_elimination_efficiency(self, score_distribution: Dict[int, int], total_solutions: int) -> Dict[int, float]`: 计算每个可能得分的消除效率。
