from collections import Counter


def frequency_analysis(ciphertext):
    """
    Perform letter-frequency analysis on ciphertext.

    Returns:
        list: A list of tuples containing:
              (letter, count, percentage)
              sorted by frequency in descending order.
    """

    # Consider only alphabetic characters
    letters = [
        char.upper()
        for char in ciphertext
        if char.isalpha()
    ]

    total_letters = len(letters)

    if total_letters == 0:
        return []

    frequency = Counter(letters)

    results = []

    for letter, count in frequency.most_common():
        percentage = (count / total_letters) * 100
        results.append((letter, count, percentage))

    return results


def display_frequency_analysis(ciphertext):
    """
    Display letter-frequency analysis in a readable format.
    """

    results = frequency_analysis(ciphertext)

    print("\nLETTER FREQUENCY ANALYSIS")
    print("-" * 40)
    print(f"{'Letter':<10}{'Count':<10}{'Percentage':<12}")
    print("-" * 40)

    for letter, count, percentage in results:
        print(f"{letter:<10}{count:<10}{percentage:.2f}%")