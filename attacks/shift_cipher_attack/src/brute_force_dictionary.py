from pathlib import Path
import re
import sys

sys.path.append(str(Path(__file__).resolve().parent))
from shift_cipher import brute_force


def load_dictionary(path):
    """Load lowercase alphabetic words from a dictionary file."""
    words = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if re.fullmatch(r'[a-z]+', word):
                words.add(word)
    return words


def score_plaintext(text, dictionary):
    """Score plaintext by the number of dictionary words it contains."""
    tokens = re.findall(r'[A-Za-z]+', text.lower())
    return sum(word in dictionary for word in tokens)


def dictionary_attack(ciphertext, dictionary_path):
    dictionary = load_dictionary(dictionary_path)
    candidates = []
    for key, plaintext in brute_force(ciphertext):
        score = score_plaintext(plaintext, dictionary)
        candidates.append((score, key, plaintext))
    candidates.sort(key=lambda x: (-x[0], x[1]))
    return candidates


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    dictionary_path = root / 'dictionary' / 'english_words.txt'
    ciphertext = 'KHOOR ZRUOG'
    for score, key, plaintext in dictionary_attack(ciphertext, dictionary_path):
        print(f'key={key:2d} score={score:2d} plaintext={plaintext}')