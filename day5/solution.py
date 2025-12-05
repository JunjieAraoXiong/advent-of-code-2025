"""
Day 5: Cafeteria
----------------
Problem: Determine which ingredient IDs are fresh based on ID ranges.

An ingredient is fresh if its ID falls into ANY of the given ranges.
Ranges are inclusive and can overlap.

Part 1: Count how many available ingredient IDs are fresh
"""


def parse_input(input_file):
    """
    Parse input into fresh ranges and available ingredient IDs.

    Returns:
        ranges: list of (start, end) tuples
        ingredients: list of ingredient IDs to check
    """
    with open(input_file, 'r') as f:
        content = f.read().strip()

    # Split by blank line
    parts = content.split('\n\n')

    # Parse ranges
    ranges = []
    for line in parts[0].strip().split('\n'):
        start, end = line.split('-')
        ranges.append((int(start), int(end)))

    # Parse ingredient IDs
    ingredients = []
    for line in parts[1].strip().split('\n'):
        ingredients.append(int(line))

    return ranges, ingredients


def is_fresh(ingredient_id, ranges):
    """Check if an ingredient ID falls into any fresh range."""
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def merge_ranges(ranges):
    """
    Merge overlapping ranges for more efficient checking.

    This optimization is helpful when we have many ranges that overlap.
    """
    if not ranges:
        return []

    # Sort by start value
    sorted_ranges = sorted(ranges, key=lambda x: x[0])

    merged = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # Check if ranges overlap or are adjacent
        if start <= last_end + 1:
            # Merge by extending the end if necessary
            merged[-1] = (last_start, max(last_end, end))
        else:
            # No overlap, add as new range
            merged.append((start, end))

    return merged


def is_fresh_binary_search(ingredient_id, merged_ranges):
    """
    Check if ingredient ID is fresh using binary search on merged ranges.

    More efficient for large number of queries.
    """
    left, right = 0, len(merged_ranges) - 1

    while left <= right:
        mid = (left + right) // 2
        start, end = merged_ranges[mid]

        if start <= ingredient_id <= end:
            return True
        elif ingredient_id < start:
            right = mid - 1
        else:  # ingredient_id > end
            left = mid + 1

    return False


def solve_part1(input_file):
    """Count how many available ingredient IDs are fresh."""
    ranges, ingredients = parse_input(input_file)

    # Merge ranges for efficient lookup
    merged = merge_ranges(ranges)

    fresh_count = 0
    for ingredient_id in ingredients:
        if is_fresh_binary_search(ingredient_id, merged):
            fresh_count += 1

    return fresh_count


def solve_part2(input_file):
    """
    Count total number of unique IDs considered fresh by all ranges.

    After merging overlapping ranges, sum up the size of each range.
    Size of range (start, end) = end - start + 1 (inclusive)
    """
    ranges, _ = parse_input(input_file)

    # Merge ranges to eliminate overlaps
    merged = merge_ranges(ranges)

    # Count total IDs covered
    total_ids = 0
    for start, end in merged:
        total_ids += end - start + 1

    return total_ids


def verify_example():
    """Verify the solution with the example from the problem."""
    ranges = [
        (3, 5),
        (10, 14),
        (16, 20),
        (12, 18)
    ]

    ingredients = [1, 5, 8, 11, 17, 32]

    # Expected results:
    # 1 - spoiled (not in any range)
    # 5 - fresh (in 3-5)
    # 8 - spoiled
    # 11 - fresh (in 10-14)
    # 17 - fresh (in 16-20 and 12-18)
    # 32 - spoiled

    merged = merge_ranges(ranges)
    print("Example verification:")
    print(f"  Original ranges: {ranges}")
    print(f"  Merged ranges: {merged}")
    print()

    fresh_count = 0
    for ing_id in ingredients:
        is_f = is_fresh_binary_search(ing_id, merged)
        status = "fresh" if is_f else "spoiled"
        print(f"  ID {ing_id}: {status}")
        if is_f:
            fresh_count += 1

    print()
    print(f"  Fresh count: {fresh_count}")
    print(f"  Expected: 3")
    print(f"  Match: {fresh_count == 3}")

    return fresh_count == 3


if __name__ == "__main__":
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "inputs.txt")

    # Verify Part 2 example: ranges 3-5, 10-14, 16-20, 12-18
    # Merged: 3-5, 10-20 -> (5-3+1) + (20-10+1) = 3 + 11 = 14
    example_ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
    merged = merge_ranges(example_ranges)
    example_count = sum(end - start + 1 for start, end in merged)
    assert example_count == 14, f"Example failed: got {example_count}, expected 14"

    print("Day 5: Cafeteria")
    print("-" * 30)
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")
