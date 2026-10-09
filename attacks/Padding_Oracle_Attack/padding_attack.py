from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16


# Partner 1: Encryption and padding oracle


def pad(data):
    padding_length = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding_length]) * padding_length


def unpad(data):
    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Invalid padding")

    padding_length = data[-1]

    if not 1 <= padding_length <= BLOCK_SIZE:
        raise ValueError("Invalid padding")

    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Invalid padding")

    return data[:-padding_length]


def encrypt(plaintext):
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext))

    return key, iv, ciphertext


def padding_oracle(key, iv, ciphertext):
    """Return only whether decrypted PKCS#7 padding is valid."""
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        unpad(plaintext)
        return True
    except ValueError:
        return False


# Partner 2: Implement the attack and query counter here.
# Required interface:
# recover_plaintext(iv, ciphertext, oracle)
#
# The recovery function must not receive or access the AES key.


def main():
    original_plaintext = b"Padding oracle attack lab demonstration"

    key, iv, ciphertext = encrypt(original_plaintext)

    print("Original plaintext:", original_plaintext.decode())
    print("IV:", iv.hex())
    print("Ciphertext:", ciphertext.hex())
    print("Oracle accepts original ciphertext:", padding_oracle(
        key, iv, ciphertext
    ))


if __name__ == "__main__":
    main()