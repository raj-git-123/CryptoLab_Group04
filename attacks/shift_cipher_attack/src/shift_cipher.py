ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def encrypt(text, key):
    """Encrypt alphabetic characters using a Caesar/shift cipher."""
    key %= 26
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + key) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def decrypt(text, key):
    """Decrypt alphabetic characters using a Caesar/shift cipher."""
    return encrypt(text, -key)


def brute_force(text):
    """Return all 26 possible plaintexts, indexed by encryption key."""
    return [(key, decrypt(text, key)) for key in range(26)]


if __name__ == '__main__':
    sample = 'HELLO WORLD'
    key = 3
    cipher = encrypt(sample, key)
    print('Plaintext :', sample)
    print('Ciphertext:', cipher)
    print('Decrypted :', decrypt(cipher, key))