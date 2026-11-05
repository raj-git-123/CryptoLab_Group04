
import random
import string

# Encryption and decryption using MT19937
def encrypt_decrypt(data, seed):
    random.seed(seed)

    result = bytearray()

    for byte in data:
        key = random.getrandbits(8)
        result.append(byte ^ key)

    return bytes(result)


# Test encryption and decryption
message = b"Hello Cryptography Lab"

seed = 12345
# a seed initialize prng 
# same seed, same sequence always

ciphertext = encrypt_decrypt(message, seed)
decrypted = encrypt_decrypt(ciphertext, seed)

print("Original message:", message.decode())
print("Ciphertext:", ciphertext.hex())
print("Decrypted message:", decrypted.decode())


# Generate plaintext with random prefix
prefix_length = random.randint(5, 20)

prefix = ''.join(
    random.choices(string.printable[:95], k=prefix_length)
)

plaintext = (prefix + "A" * 14).encode()

print("\nGenerated plaintext:", plaintext.decode())


# Encrypt using a random 16-bit seed
secret_seed = random.randint(0, 65535)

ciphertext = encrypt_decrypt(plaintext, secret_seed)

print("Ciphertext:", ciphertext.hex())


# Brute-force all 16-bit seeds
known_sequence = b"A" * 14

recovered = False

for guess in range(65536):

    decrypted_text = encrypt_decrypt(ciphertext, guess)

    # Check whether the known sequence exists
    if known_sequence in decrypted_text:

        print("\nMatching seed found:", guess)
        print("Recovered plaintext:", decrypted_text.decode())

        # 5. Verify the recovered seed
        check = encrypt_decrypt(ciphertext, guess)

        if check == decrypted_text and known_sequence in check:
            print("Verification successful!")
            print("Complete ciphertext decrypted correctly.")

        recovered = True
        break

if not recovered:
    print("No matching seed found.")
