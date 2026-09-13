from pathlib import Path

from frequency_analysis import frequency_analysis
from word_frequency_analysis import (
    word_frequency_analysis,
    analyze_word_lengths
)
from pattern_analysis import pattern_analysis


def read_file(filename):
    """Read and return the contents of a text file."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def display_frequency_results(ciphertext):
    """Display letter-frequency analysis."""

    results = frequency_analysis(ciphertext)

    print("\n" + "=" * 60)
    print("LETTER FREQUENCY ANALYSIS")
    print("=" * 60)

    print(f"{'Letter':<10}{'Count':<10}{'Percentage':<12}")
    print("-" * 60)

    for letter, count, percentage in results:
        print(f"{letter:<10}{count:<10}{percentage:.2f}%")


def display_word_results(ciphertext):
    """Display word-frequency analysis."""

    frequencies = word_frequency_analysis(ciphertext)
    lengths = analyze_word_lengths(ciphertext)

    print("\n" + "=" * 60)
    print("WORD FREQUENCY ANALYSIS")
    print("=" * 60)

    print("\nMost Frequent Words")
    print("-" * 40)

    print(f"{'Word':<20}{'Count':<10}")

    for word, count in frequencies[:20]:
        print(f"{word:<20}{count:<10}")

    print("\nWord Length Distribution")
    print("-" * 40)

    print(f"{'Length':<20}{'Count':<10}")

    for length, count in lengths.items():
        print(f"{length:<20}{count:<10}")


def display_pattern_results(ciphertext):
    """Display repeated-letter patterns."""

    patterns = pattern_analysis(ciphertext)

    print("\n" + "=" * 60)
    print("PATTERN ANALYSIS")
    print("=" * 60)

    for pattern, words in sorted(
        patterns.items(),
        key=lambda item: (len(item[0]), item[0])
    ):
        print(
            f"{pattern}: "
            f"{', '.join(words[:10])}"
        )


def main():

    # Locate the substitution_cipher directory
    base_dir = Path(__file__).resolve().parent.parent

    ciphertext_file = (
        base_dir / "outputs" / "ciphertext.txt"
    )

    # Read ciphertext
    ciphertext = read_file(ciphertext_file)

    print("=" * 60)
    print("MONOALPHABETIC SUBSTITUTION CIPHER ANALYSIS")
    print("=" * 60)

    print(f"\nCiphertext length: {len(ciphertext)} characters")

    display_frequency_results(ciphertext)

    display_word_results(ciphertext)

    display_pattern_results(ciphertext)


if __name__ == "__main__":
    main()