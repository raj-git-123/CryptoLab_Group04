from collections import defaultdict
import re


def get_pattern(word):
    """
    Convert a word into its repeated-letter pattern.

    Example:
        HELLO -> 0 1 2 2 3
        APPLE -> 0 1 1 2 3
        TEST  -> 0 1 2 0
    """

    word = word.upper()

    mapping = {}
    next_number = 0
    pattern = []

    for char in word:
        if char not in mapping:
            mapping[char] = next_number
            next_number += 1

        pattern.append(mapping[char])

    return tuple(pattern)


def extract_words(ciphertext):
    """
    Extract alphabetic words from ciphertext.
    """

    return re.findall(r"[A-Za-z]+", ciphertext.upper())


def pattern_analysis(ciphertext):
    """
    Group ciphertext words according to their repeated-letter patterns.

    Returns:
        dict: pattern -> list of words
    """

    words = extract_words(ciphertext)

    patterns = defaultdict(list)

    for word in words:
        pattern = get_pattern(word)

        if word not in patterns[pattern]:
            patterns[pattern].append(word)

    return dict(patterns)


def display_pattern_analysis(ciphertext):
    """
    Display repeated-letter patterns found in ciphertext.
    """

    patterns = pattern_analysis(ciphertext)

    print("\nPATTERN ANALYSIS")
    print("-" * 60)

    for pattern, words in sorted(
        patterns.items(),
        key=lambda item: (len(item[0]), item[0])
    ):
        print(f"Pattern {pattern}: {', '.join(words)}")