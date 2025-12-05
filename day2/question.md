# Day 2: Gift Shop

## Story

You get inside and take the elevator to its only other stop: the gift shop. "Thank you for visiting the North Pole!" gleefully exclaims a nearby sign. You aren't sure who is even allowed to visit the North Pole, but you know you can access the lobby through here, and from there you can access the rest of the North Pole base.

As you make your way through the surprisingly extensive selection, one of the clerks recognizes you and asks for your help.

## Problem

One of the younger Elves was playing on a gift shop computer and managed to add a whole bunch of invalid product IDs to their gift shop database! You need to identify the invalid product IDs.

### Input Format

Product ID ranges separated by commas, each range gives first ID and last ID separated by a dash:
```
11-22,95-115,998-1012,...
```

### Invalid ID Definition

An ID is **invalid** if it is made only of some sequence of digits **repeated twice**:
- `55` (5 twice)
- `6464` (64 twice)
- `123123` (123 twice)

**Note:** No leading zeroes. `0101` isn't an ID at all. `101` is a valid ID.

## Part 1

Find all invalid IDs in the given ranges and add them up.

### Example

```
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
```

- `11-22` has two invalid IDs: 11, 22
- `95-115` has one invalid ID: 99
- `998-1012` has one invalid ID: 1010
- `1188511880-1188511890` has one invalid ID: 1188511885
- `222220-222224` has one invalid ID: 222222
- `1698522-1698528` contains no invalid IDs
- `446443-446449` has one invalid ID: 446446
- `38593856-38593862` has one invalid ID: 38593859
- The rest contain no invalid IDs

Sum = **1227775554**
