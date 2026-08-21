from pathlib import Path
import math
import re
import sys

sys.path.append(str(Path(__file__).resolve().parent))
from shift_cipher import brute_force

ENGLISH_FREQUENCIES = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}


def chi_square(text):
    letters = [c for c in text.upper() if c.isalpha()]
    n = len(letters)
    if n == 0:
        return float('inf')

    counts = {c: 0 for c in ENGLISH_FREQUENCIES}
    for c in letters:
        counts[c] += 1

    statistic = 0.0
    for c, freq in ENGLISH_FREQUENCIES.items():
        expected = n * freq / 100.0
        observed = counts[c]
        if expected > 0:
            statistic += (observed - expected) ** 2 / expected
    return statistic


def chi_square_attack(ciphertext):
    candidates = []
    for key, plaintext in brute_force(ciphertext):
        score = chi_square(plaintext)
        candidates.append((score, key, plaintext))
    candidates.sort(key=lambda x: (x[0], x[1]))
    return candidates


if __name__ == '__main__':
    ciphertext = 'KHOOR ZRUOG'
    for score, key, plaintext in chi_square_attack(ciphertext)[:5]:
        print(f'key={key:2d} chi_square={score:8.3f} plaintext={plaintext}')
