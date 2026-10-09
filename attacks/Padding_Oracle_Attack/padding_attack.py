from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from padding_recovery import recover_plaintext

BLOCK_SIZE = 16

query_count = 0


def pad(data):
    """Apply PKCS#7 padding."""
    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([padding_length]) * padding_length


def unpad(data):
    """Remove and validate PKCS#7 padding."""
    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Invalid padding")

    padding_length = data[-1]

    if not 1 <= padding_length <= BLOCK_SIZE:
        raise ValueError("Invalid padding")

    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Invalid padding")

    return data[:-padding_length]


def encrypt(plaintext):
    """Encrypt plaintext using AES-CBC."""
    key = get_random_bytes(16)
    iv = get_random_bytes(BLOCK_SIZE)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext))

    return key, iv, ciphertext


def padding_oracle(key, iv, ciphertext):
    """
    Simulated oracle: return True if decrypted data has valid
    PKCS#7 padding, otherwise return False.
    """
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        unpad(plaintext)
        return True

    except ValueError:
        return False


def oracle_adapter(key, crafted_iv, target_block):
    """Test one ciphertext block using a crafted IV."""
    return padding_oracle(key, crafted_iv, target_block)


def main():
    global query_count
    query_count = 0

    original_plaintext = b"Padding oracle attack lab demonstration"

    # Generate key, IV and ciphertext.
    key, iv, ciphertext = encrypt(original_plaintext)

    print("Original plaintext:", original_plaintext.decode())
    print("IV:", iv.hex())
    print("Ciphertext:", ciphertext.hex())

    # Check the oracle against the original ciphertext.
    valid = padding_oracle(key, iv, ciphertext)
    print("Oracle accepts original ciphertext:", valid)

    # Count oracle queries made by the attack.
    def counted_oracle(crafted_iv, target_block):
        global query_count
        query_count += 1

        return oracle_adapter(key, crafted_iv, target_block)

    # Recover plaintext without passing the key to the attack.
    recovered = recover_plaintext(
        iv,
        ciphertext,
        counted_oracle
    )

    print("Recovered plaintext:", recovered.decode())
    print("Oracle queries:", query_count)
    print("Recovery successful:", recovered == original_plaintext)


if __name__ == "__main__":
    main()
