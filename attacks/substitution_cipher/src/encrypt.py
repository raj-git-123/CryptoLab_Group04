from pathlib import Path

from substitution_cipher import generate_key, encrypt


def read_file(filename):
    """Read and return the contents of a text file."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def write_file(filename, content):
    """Write content to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def main():
    # Get the substitution_cipher directory
    base_dir = Path(__file__).resolve().parent.parent

    plaintext_file = base_dir / "testcases" / "plaintext.txt"
    ciphertext_file = base_dir / "outputs" / "ciphertext.txt"
    key_file = base_dir / "outputs" / "original_key.txt"

    # Generate a reproducible substitution key
    key = generate_key(seed=2026)

    # Read plaintext
    plaintext = read_file(plaintext_file)

    # Encrypt plaintext
    ciphertext = encrypt(plaintext, key)

    # Save ciphertext
    write_file(ciphertext_file, ciphertext)

    # Save original key for later verification
    write_file(key_file, key)

    print("Monoalphabetic substitution encryption completed.")
    print()
    print("Substitution Key:")
    print(key)
    print()
    print("Ciphertext saved to:")
    print(ciphertext_file)


if __name__ == "__main__":
    main()