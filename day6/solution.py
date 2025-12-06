"""
Day 6: Trash Compactor
----------------------
Problem: Parse a math worksheet where problems are arranged vertically.

Part 1: Numbers are read horizontally per row, problems left-to-right
Part 2: Numbers are read vertically per column (top=MSD, bottom=LSD),
        problems right-to-left (cephalopod math!)
"""


def parse_input(input_file):
    """
    Parse the worksheet into a list of problems.
    Each problem is (operator, [numbers])
    """
    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # Pad all lines to same length
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    # The last line contains operators
    operator_line = lines[-1]
    number_lines = lines[:-1]

    problems = []
    col = 0

    while col < max_len:
        # Skip separator columns (all spaces)
        if all(line[col] == ' ' for line in lines):
            col += 1
            continue

        # Find the end of this problem (next all-space column or end)
        start_col = col
        while col < max_len and not all(line[col] == ' ' for line in lines):
            col += 1
        end_col = col

        # Extract this problem
        # Get the operator (find * or + in the operator line segment)
        op_segment = operator_line[start_col:end_col]
        operator = '*' if '*' in op_segment else '+'

        # Get the numbers from each row
        numbers = []
        for line in number_lines:
            segment = line[start_col:end_col].strip()
            if segment:
                numbers.append(int(segment))

        if numbers:
            problems.append((operator, numbers))

    return problems


def solve_problem(operator, numbers):
    """Solve a single problem."""
    if operator == '+':
        return sum(numbers)
    else:  # '*'
        result = 1
        for n in numbers:
            result *= n
        return result


def solve_part1(input_file):
    """Solve all problems and return the grand total."""
    problems = parse_input(input_file)

    grand_total = 0
    for operator, numbers in problems:
        result = solve_problem(operator, numbers)
        grand_total += result

    return grand_total


def parse_input_part2(input_file):
    """
    Parse the worksheet for Part 2 (cephalopod math).

    Numbers are read vertically column by column:
    - Each column within a problem represents one digit
    - Top row = most significant digit, bottom row = least significant
    - Read digits in each column to form numbers
    - Problems are read right-to-left
    """
    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # Pad all lines to same length
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    # The last line contains operators
    operator_line = lines[-1]
    number_lines = lines[:-1]

    problems = []
    col = 0

    while col < max_len:
        # Skip separator columns (all spaces)
        if all(line[col] == ' ' for line in lines):
            col += 1
            continue

        # Find the end of this problem (next all-space column or end)
        start_col = col
        while col < max_len and not all(line[col] == ' ' for line in lines):
            col += 1
        end_col = col

        # Extract this problem
        # Get the operator (find * or + in the operator line segment)
        op_segment = operator_line[start_col:end_col]
        operator = '*' if '*' in op_segment else '+'

        # For Part 2: Read each column as a vertical number
        # Each column within the problem is a separate number
        numbers = []
        for c in range(start_col, end_col):
            # Read digits from top to bottom for this column
            digits = ""
            for line in number_lines:
                char = line[c]
                if char.isdigit():
                    digits += char
            if digits:
                numbers.append(int(digits))

        if numbers:
            problems.append((operator, numbers))

    # Reverse the problems (right-to-left reading)
    problems.reverse()

    return problems


def solve_part2(input_file):
    """Solve all problems using cephalopod math and return the grand total."""
    problems = parse_input_part2(input_file)

    grand_total = 0
    for operator, numbers in problems:
        result = solve_problem(operator, numbers)
        grand_total += result

    return grand_total


def verify_example_part2():
    """Verify Part 2 with the example from the problem."""
    # Example in cephalopod math (right-to-left, vertical digits):
    # Rightmost: 4 + 431 + 623 = 1058
    # Second: 175 * 581 * 32 = 3253600
    # Third: 8 + 248 + 369 = 625
    # Leftmost: 356 * 24 * 1 = 8544
    # Grand total = 3263827

    problems = [
        ('+', [4, 431, 623]),      # rightmost
        ('*', [175, 581, 32]),     # second from right
        ('+', [8, 248, 369]),      # third from right
        ('*', [356, 24, 1])        # leftmost
    ]

    # Reverse to match our parsing order (we parse left-to-right then reverse)
    problems = list(reversed(problems))

    results = []
    for op, nums in reversed(problems):  # Print right-to-left
        r = solve_problem(op, nums)
        results.append(r)
        print(f"  {' {} '.format(op).join(map(str, nums))} = {r}")

    total = sum(results)
    print(f"  Grand total: {total}")
    print(f"  Expected: 3263827")
    print(f"  Match: {total == 3263827}")

    return total == 3263827


if __name__ == "__main__":
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "inputs.txt")

    print("Day 6: Trash Compactor")
    print("-" * 30)
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")
