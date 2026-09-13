import string
import random


ALPHABET = string.ascii_uppercase


def generate_key(seed=None):
    """
    Generate a random monoalphabetic substitution key.

    Returns:
        str: A permutation of the uppercase English alphabet.
    """

    alphabet = list(ALPHABET)

    if seed is not None:
        random.seed(seed)

    random.shuffle(alphabet)

    return ''.join(alphabet)


def validate_key(key):
    """
    Validate whether the key is a valid monoalphabetic substitution key.

    A valid key must:
    - contain exactly 26 characters
    - contain every alphabet letter exactly once
    """

    key = key.upper()

    return (
        len(key) == 26
        and set(key) == set(ALPHABET)
    )


def apply_substitution(text, key):
    """
    Apply a substitution key to the given text.

    Alphabetic characters are substituted.
    Spaces, punctuation, digits and other characters remain unchanged.
    """

    key = key.upper()

    if not validate_key(key):
        raise ValueError("Invalid substitution key.")

    result = []

    for char in text:
        if char.isalpha():
            if char.isupper():
                result.append(key[ord(char) - ord('A')])
            else:
                result.append(key[ord(char.upper()) - ord('A')].lower())
        else:
            result.append(char)

    return ''.join(result)


def encrypt(plaintext, key):
    """
    Encrypt plaintext using the monoalphabetic substitution cipher.
    """

    return apply_substitution(plaintext, key)


def decrypt(ciphertext, key):
    """
    Decrypt ciphertext using the monoalphabetic substitution key.
    """

    key = key.upper()

    if not validate_key(key):
        raise ValueError("Invalid substitution key.")

    reverse_key = {}

    for i in range(26):
        reverse_key[key[i]] = ALPHABET[i]

    result = []

    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                result.append(reverse_key[char])
            else:
                result.append(reverse_key[char.upper()].lower())
        else:
            result.append(char)

    return ''.join(result)