# MCQ-solution-finder

## Description

MCQ-solution-finder is a Python program designed to help users find possible solutions to multiple choice questions (MCQs) based on their solution attempts and scores. The program allows users to input the number of questions and options per question, add solution attempts with scores, and find possible solutions.

MCQ-solution-finder 是一个 Python 程序，旨在帮助用户根据他们的解答尝试和得分找到多项选择题（MCQ）的可能解答。该程序允许用户输入问题数量和每个问题的选项数量，添加带有得分的解答尝试，并找到可能的解答。

## Usage Instructions

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

1. 克隆仓库：
   ```
   git clone https://github.com/YinChingZ/MCQ-solution-finder.git
   cd MCQ-solution-finder
   ```

2. 确保您已安装 Python（版本 3.6 或更高）。

3. 运行主脚本：
   ```
   python main.py
   ```

4. 按照屏幕上的说明与程序交互：
   - 输入问题数量。
   - 输入每个问题的选项数量（例如，'4' 表示所有问题都有 ABCD 选项，或 '4,5,4' 表示不同问题有不同数量的选项）。
   - 从菜单选项中选择添加带有得分的解答尝试、查找可能的解答或退出程序。

## Potential Issues and Troubleshooting

### Performance Limitations

The program has a performance limitation due to the maximum number of solutions stored (`max_solutions_to_store` is set to 1000). If the number of consistent solutions exceeds this limit, the program may not be able to find all possible solutions. To address this issue, consider increasing the `max_solutions_to_store` value in `mcq_solver.py` or optimizing the solution-finding algorithm.

该程序由于存储的最大解答数量（`max_solutions_to_store` 设置为 1000）而存在性能限制。如果一致解答的数量超过此限制，程序可能无法找到所有可能的解答。为了解决此问题，可以考虑增加 `mcq_solver.py` 中的 `max_solutions_to_store` 值或优化解答查找算法。

### Handling Different Option Counts per Question

The program supports different option counts per question. However, if the input for the number of options per question is not consistent with the number of questions, the program will display an error message. Ensure that the input for the number of options per question matches the number of questions.

该程序支持每个问题的不同选项数量。但是，如果每个问题的选项数量输入与问题数量不一致，程序将显示错误消息。确保每个问题的选项数量输入与问题数量匹配。

### Dependencies

The program does not have any external dependencies. It uses standard Python libraries.

该程序没有任何外部依赖。它使用标准的 Python 库。

### Troubleshooting Steps

- If you encounter any issues while running the program, ensure that you have the correct version of Python installed.
- Check for any error messages displayed by the program and follow the instructions provided.
- If the program is not behaving as expected, review the input values for the number of questions and options per question to ensure they are correct.

- 如果在运行程序时遇到任何问题，请确保已安装正确版本的 Python。
- 检查程序显示的任何错误消息并按照提供的说明进行操作。
- 如果程序未按预期运行，请检查问题数量和每个问题的选项数量的输入值，以确保它们是正确的。
