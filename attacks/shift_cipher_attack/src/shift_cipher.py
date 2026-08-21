def encrypt(plaintext, key):
    result = ""

    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - ord('A') + key) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') + key) % 26 + ord('a'))
        else:
            result += char

    return result


def decrypt(ciphertext, key):
    return encrypt(ciphertext, -key)


if __name__ == "__main__":
    plaintext = "THE QUICK BROWN FOX"
    key = 3

    ciphertext = encrypt(plaintext, key)
    decrypted = decrypt(ciphertext, key)

    print("Plaintext :", plaintext)
    print("Key       :", key)
    print("Ciphertext:", ciphertext)
    print("Decrypted :", decrypted)