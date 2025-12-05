"""
Advent of Code 2025 - Day 3: Lobby
Solution for Part 1 and Part 2

Problem: Given banks of batteries (each line is a bank), find the maximum
joltage you can produce by selecting exactly K batteries.
The joltage is the number formed by the selected batteries' digits (in order).

Part 1: K = 2
Part 2: K = 12

Key insight (greedy approach):
To maximize an N-digit number, greedily pick the largest possible digit at each position,
while ensuring enough digits remain to fill the remaining positions.
"""


def max_joltage_k(bank, k):
    """
    Find the maximum joltage from a bank by selecting exactly k batteries.

    Greedy strategy:
    - For position 1 of k digits, we can pick from bank[0] to bank[n-k]
      (must leave k-1 digits after for remaining positions)
    - Pick the largest digit in that range
    - For position 2, we can pick from after the first pick to bank[n-k+1]
    - Continue until all k positions are filled

    This works because we want to maximize the leftmost digits first.
    """
    n = len(bank)
    result = []
    start = 0  # Earliest position we can pick from

    for i in range(k):
        # For the i-th digit (0-indexed), we need k-i-1 more digits after this one
        # So we can pick from positions start to n-(k-i-1)-1 = n-k+i
        end = n - k + i

        # Find the maximum digit in range [start, end]
        best_pos = start
        best_digit = bank[start]
        for pos in range(start, end + 1):
            if bank[pos] > best_digit:
                best_digit = bank[pos]
                best_pos = pos

        result.append(best_digit)
        start = best_pos + 1  # Next digit must come after this one

    return int(''.join(result))


def max_joltage(bank):
    """
    Find the maximum joltage from a bank of batteries.

    Strategy:
    - We need to pick two positions i < j to form a two-digit number bank[i]bank[j]
    - To maximize, we want the largest possible first digit, then the largest
      possible second digit that comes after it

    Approach:
    - For each position i, find the maximum digit that appears after position i
    - The candidate joltage is bank[i] * 10 + max_after[i]
    - Return the maximum of all candidates
    """
    n = len(bank)

    # Precompute: max_after[i] = maximum digit in bank[i+1:]
    max_after = [0] * n
    max_so_far = 0
    for i in range(n - 1, -1, -1):
        max_after[i] = max_so_far
        max_so_far = max(max_so_far, int(bank[i]))

    # Find maximum joltage
    best = 0
    for i in range(n - 1):  # Can't pick last position as first digit
        first_digit = int(bank[i])
        second_digit = max_after[i]
        joltage = first_digit * 10 + second_digit
        best = max(best, joltage)

    return best


def solve_part1(input_file):
    """
    Sum the maximum joltage from each bank (k=2).
    """
    with open(input_file, 'r') as f:
        banks = f.read().strip().split('\n')

    total = 0
    for bank in banks:
        total += max_joltage_k(bank, 2)

    return total


def solve_part2(input_file):
    """
    Sum the maximum joltage from each bank (k=12).
    """
    with open(input_file, 'r') as f:
        banks = f.read().strip().split('\n')

    total = 0
    for bank in banks:
        total += max_joltage_k(bank, 12)

    return total


if __name__ == "__main__":
    # Test with example
    example = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111"
    ]

    print("=== Part 1 Example ===")
    example_total = 0
    for bank in example:
        mj = max_joltage_k(bank, 2)
        print(f"{bank}: {mj}")
        example_total += mj
    print(f"Example total: {example_total}")
    print()

    print("=== Part 2 Example ===")
    example_total_p2 = 0
    for bank in example:
        mj = max_joltage_k(bank, 12)
        print(f"{bank}: {mj}")
        example_total_p2 += mj
    print(f"Example total: {example_total_p2}")
    print()

    # Solve actual puzzle
    result1 = solve_part1("inputs.txt")
    print(f"Part 1: {result1}")

    result2 = solve_part2("inputs.txt")
    print(f"Part 2: {result2}")
