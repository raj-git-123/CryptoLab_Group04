from collections import Counter
import re


def extract_words(ciphertext):
    """
    Extract alphabetic words from ciphertext.

    Returns:
        list: Words converted to uppercase.
    """

    return re.findall(r"[A-Za-z]+", ciphertext.upper())


def word_frequency_analysis(ciphertext):
    """
    Analyze word frequencies in ciphertext.

    Returns:
        list: (word, count) sorted by frequency descending.
    """

    words = extract_words(ciphertext)

    frequency = Counter(words)

    return frequency.most_common()


def analyze_word_lengths(ciphertext):
    """
    Analyze the frequency of words based on their lengths.

    Returns:
        dict: word length -> frequency
    """

    words = extract_words(ciphertext)

    length_frequency = Counter(len(word) for word in words)

    return dict(sorted(length_frequency.items()))


def display_word_frequency_analysis(ciphertext):
    """
    Display word-frequency information.
    """

    words = extract_words(ciphertext)
    frequencies = word_frequency_analysis(ciphertext)
    length_frequency = analyze_word_lengths(ciphertext)

    print("\nWORD FREQUENCY ANALYSIS")
    print("-" * 40)

    print(f"Total words: {len(words)}")
    print(f"Unique words: {len(set(words))}")

    print("\nMost Frequent Words")
    print("-" * 40)
    print(f"{'Word':<15}{'Count':<10}")
    print("-" * 40)

    for word, count in frequencies[:20]:
        print(f"{word:<15}{count:<10}")

    print("\nWord Length Distribution")
    print("-" * 40)
    print(f"{'Length':<15}{'Count':<10}")
    print("-" * 40)

    for length, count in length_frequency.items():
        print(f"{length:<15}{count:<10}")