# Day 1: Secret Entrance

## Story

The Elves have good news and bad news.

The good news is that they've discovered project management! This has given them the tools they need to prevent their usual Christmas emergency. For example, they now know that the North Pole decorations need to be finished soon so that other critical tasks can start on time.

The bad news is that they've realized they have a different emergency: according to their resource planning, none of them have any time left to decorate the North Pole!

To save Christmas, the Elves need you to finish decorating the North Pole by December 12th.

## Problem

You arrive at the secret entrance to the North Pole base ready to start decorating. Unfortunately, the password seems to have been changed, so you can't get in. A document taped to the wall helpfully explains:

> "Due to new security protocols, the password is locked in the safe below. Please see the attached document for the new combination."

The safe has a dial with only an arrow on it; around the dial are the numbers 0 through 99 in order. As you turn the dial, it makes a small click noise as it reaches each number.

The attached document (your puzzle input) contains a sequence of rotations, one per line, which tell you how to open the safe:
- A rotation starts with an `L` or `R` which indicates whether the rotation should be to the left (toward lower numbers) or to the right (toward higher numbers)
- Then, the rotation has a distance value which indicates how many clicks the dial should be rotated in that direction

### Examples

- If the dial were pointing at 11, a rotation of `R8` would cause the dial to point at 19. After that, a rotation of `L19` would cause it to point at 0.
- Because the dial is a circle, turning the dial left from 0 one click makes it point at 99. Similarly, turning the dial right from 99 one click makes it point at 0.
- If the dial were pointing at 5, a rotation of `L10` would cause it to point at 95. After that, a rotation of `R5` would cause it to point at 0.

**The dial starts by pointing at 50.**

## The Trick

The safe is actually a decoy. The actual password is **the number of times the dial is left pointing at 0 after any rotation in the sequence**.

## Example Walkthrough

Given these rotations:
```
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
```

Following these rotations would cause the dial to move as follows:

1. The dial starts by pointing at 50.
2. The dial is rotated L68 to point at 82.
3. The dial is rotated L30 to point at 52.
4. The dial is rotated R48 to point at **0**. ✓
5. The dial is rotated L5 to point at 95.
6. The dial is rotated R60 to point at 55.
7. The dial is rotated L55 to point at **0**. ✓
8. The dial is rotated L1 to point at 99.
9. The dial is rotated L99 to point at **0**. ✓
10. The dial is rotated R14 to point at 14.
11. The dial is rotated L82 to point at 32.

Because the dial points at 0 a total of **three times** during this process, the password in this example is **3**.

## Part 1

Analyze the rotations in your attached document. What's the actual password to open the door?

## Part 2

Using "method 0x434C49434B" means counting the number of times **any click** causes the dial to point at 0, regardless of whether it happens during a rotation or at the end of one.

### Example Walkthrough (Part 2)

Using the same rotations:

1. The dial starts by pointing at 50.
2. The dial is rotated L68 to point at 82; during this rotation, it points at 0 **once**.
3. The dial is rotated L30 to point at 52.
4. The dial is rotated R48 to point at **0**.
5. The dial is rotated L5 to point at 95.
6. The dial is rotated R60 to point at 55; during this rotation, it points at 0 **once**.
7. The dial is rotated L55 to point at **0**.
8. The dial is rotated L1 to point at 99.
9. The dial is rotated L99 to point at **0**.
10. The dial is rotated R14 to point at 14.
11. The dial is rotated L82 to point at 32; during this rotation, it points at 0 **once**.

The dial points at 0 three times at the end of a rotation, plus three more times during a rotation. So the new password would be **6**.

**Note:** If the dial were pointing at 50, a single rotation like R1000 would cause the dial to point at 0 ten times before returning back to 50!

Using password method 0x434C49434B, what is the password to open the door?
