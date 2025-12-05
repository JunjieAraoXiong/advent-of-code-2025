"""
Advent of Code 2025 - Day 2: Gift Shop
Solution for Part 1 and Part 2

Problem: Find all "invalid" product IDs in given ranges.

Part 1: ID is invalid if it consists of a digit sequence repeated exactly twice.
        Examples: 55 (5+5), 6464 (64+64), 123123 (123+123)

Part 2: ID is invalid if it consists of a digit sequence repeated at least twice.
        Examples: 111 (1 three times), 123123123 (123 three times), 1212121212 (12 five times)
"""


def is_invalid_id_part1(n):
    """
    Part 1: Check if a number is repeated exactly twice.
    """
    s = str(n)
    length = len(s)

    if length % 2 != 0:
        return False

    half = length // 2
    return s[:half] == s[half:]


def is_invalid_id_part2(n):
    """
    Part 2: Check if a number is a pattern repeated at least twice.

    We check all possible pattern lengths that divide the total length.
    For a number with L digits, the pattern length k must:
    1. Divide L evenly (L % k == 0)
    2. Result in at least 2 repetitions (L / k >= 2, so k <= L/2)

    Examples:
        111 -> length 3, check k=1: "1" repeated 3 times -> True
        123123 -> length 6, check k=1,2,3: k=3 works ("123" x 2) -> True
        1212121212 -> length 10, check k=1,2,5: k=2 works ("12" x 5) -> True
    """
    s = str(n)
    length = len(s)

    # Pattern must repeat at least twice, so pattern length <= length/2
    for pattern_len in range(1, length // 2 + 1):
        # Pattern length must divide total length evenly
        if length % pattern_len != 0:
            continue

        pattern = s[:pattern_len]
        repetitions = length // pattern_len

        # Check if the entire string is this pattern repeated
        if pattern * repetitions == s:
            return True

    return False


def find_invalid_ids_in_range_part1(start, end):
    """
    Part 1: Find all invalid IDs (pattern repeated exactly twice) in range.
    """
    invalid_ids = []
    end_digits = len(str(end))

    # Only even-length numbers (pattern repeated twice)
    for total_digits in range(2, end_digits + 2, 2):
        half_digits = total_digits // 2

        if half_digits == 1:
            min_half = 1
        else:
            min_half = 10 ** (half_digits - 1)

        max_half = 10 ** half_digits - 1

        for half_num in range(min_half, max_half + 1):
            half_str = str(half_num)
            invalid_id = int(half_str + half_str)

            if start <= invalid_id <= end:
                invalid_ids.append(invalid_id)

    return invalid_ids


def find_invalid_ids_in_range_part2(start, end):
    """
    Part 2: Find all invalid IDs (pattern repeated at least twice) in range.

    Generate all possible invalid IDs by:
    1. For each total digit length from 2 to max needed
    2. For each valid pattern length (divisor of total length, at most half)
    3. Generate all patterns of that length (no leading zeros)
    4. Create the invalid ID by repeating the pattern
    5. Check if it falls in range

    Use a set to avoid duplicates (e.g., 1111 can be "1"x4 or "11"x2)
    """
    invalid_ids = set()
    end_digits = len(str(end))

    # Check all possible total digit lengths
    for total_digits in range(2, end_digits + 2):
        # For each valid pattern length
        for pattern_len in range(1, total_digits // 2 + 1):
            # Pattern length must divide total length evenly
            if total_digits % pattern_len != 0:
                continue

            repetitions = total_digits // pattern_len

            # Generate all patterns of this length (no leading zeros)
            if pattern_len == 1:
                min_pattern = 1
            else:
                min_pattern = 10 ** (pattern_len - 1)

            max_pattern = 10 ** pattern_len - 1

            for pattern_num in range(min_pattern, max_pattern + 1):
                pattern_str = str(pattern_num)
                invalid_id = int(pattern_str * repetitions)

                if start <= invalid_id <= end:
                    invalid_ids.add(invalid_id)

    return list(invalid_ids)


def solve_part1(input_file):
    """
    Parse the input, find all invalid IDs in all ranges, and sum them.
    """
    with open(input_file, 'r') as f:
        data = f.read().strip()

    ranges = data.split(',')
    all_invalid_ids = []

    for r in ranges:
        start, end = map(int, r.split('-'))
        invalid_ids = find_invalid_ids_in_range_part1(start, end)
        all_invalid_ids.extend(invalid_ids)

    return sum(all_invalid_ids)


def solve_part2(input_file):
    """
    Parse the input, find all invalid IDs (at least 2 repetitions) in all ranges, and sum them.
    """
    with open(input_file, 'r') as f:
        data = f.read().strip()

    ranges = data.split(',')
    all_invalid_ids = []

    for r in ranges:
        start, end = map(int, r.split('-'))
        invalid_ids = find_invalid_ids_in_range_part2(start, end)
        all_invalid_ids.extend(invalid_ids)

    return sum(all_invalid_ids)


if __name__ == "__main__":
    # Test with example first
    example_ranges = [
        (11, 22),
        (95, 115),
        (998, 1012),
        (1188511880, 1188511890),
        (222220, 222224),
        (1698522, 1698528),
        (446443, 446449),
        (38593856, 38593862),
        (565653, 565659),
        (824824821, 824824827),
        (2121212118, 2121212124),
    ]

    print("=== Part 1 Example ===")
    example_sum_p1 = 0
    for start, end in example_ranges:
        ids = find_invalid_ids_in_range_part1(start, end)
        if ids:
            print(f"{start}-{end}: {ids}")
        example_sum_p1 += sum(ids)
    print(f"Example sum (Part 1): {example_sum_p1}")
    print()

    print("=== Part 2 Example ===")
    example_sum_p2 = 0
    for start, end in example_ranges:
        ids = find_invalid_ids_in_range_part2(start, end)
        if ids:
            print(f"{start}-{end}: {sorted(ids)}")
        example_sum_p2 += sum(ids)
    print(f"Example sum (Part 2): {example_sum_p2}")
    print()

    # Solve actual puzzle
    result1 = solve_part1("inputs.txt")
    print(f"Part 1: {result1}")

    result2 = solve_part2("inputs.txt")
    print(f"Part 2: {result2}")
