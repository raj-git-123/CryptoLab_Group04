ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def add_mapping(mapping, cipher_letter, plain_letter):
    """
    Add a cipher -> plaintext mapping.

    Returns:
        True if the mapping is valid and added.
        False if it creates a conflict.
    """

    cipher_letter = cipher_letter.upper()
    plain_letter = plain_letter.upper()

    # Validate letters
    if cipher_letter not in ALPHABET:
        raise ValueError("Invalid ciphertext letter.")

    if plain_letter not in ALPHABET:
        raise ValueError("Invalid plaintext letter.")

    # Check cipher -> plaintext conflict
    if cipher_letter in mapping:
        return mapping[cipher_letter] == plain_letter

    # Check plaintext already assigned to another cipher letter
    if plain_letter in mapping.values():
        return False

    mapping[cipher_letter] = plain_letter

    return True


def remove_mapping(mapping, cipher_letter):
    """
    Remove a mapping for a ciphertext letter.
    """

    cipher_letter = cipher_letter.upper()

    if cipher_letter in mapping:
        del mapping[cipher_letter]


def apply_partial_substitution(ciphertext, mapping):
    """
    Apply currently known substitutions.

    Unknown letters are represented using '?'.
    """

    result = []

    for char in ciphertext:

        if char.isalpha():

            upper_char = char.upper()

            if upper_char in mapping:
                replacement = mapping[upper_char]

                if char.islower():
                    replacement = replacement.lower()

                result.append(replacement)

            else:
                result.append("?")

        else:
            result.append(char)

    return "".join(result)


def display_mapping(mapping):
    """
    Display the current cipher -> plaintext mapping.
    """

    print("\nCURRENT SUBSTITUTION MAPPING")
    print("-" * 50)

    print(f"{'Cipher':<10}{'Plain':<10}")
    print("-" * 50)

    for letter in ALPHABET:

        plaintext = mapping.get(letter, "?")

        print(f"{letter:<10}{plaintext:<10}")


def is_valid_mapping(mapping):
    """
    Check whether the current mapping is one-to-one.
    """

    # No duplicate plaintext assignments
    if len(mapping.values()) != len(set(mapping.values())):
        return False

    return True