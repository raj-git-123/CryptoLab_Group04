import os
from shift_cipher import decrypt


def load_dictionary(dictionary_file):
    with open(dictionary_file, "r", encoding="utf-8") as file:
        return set(
            word.strip().lower()
            for word in file
            if word.strip()
        )


def dictionary_score(text, dictionary):
    words = text.lower().split()
    score = 0

    for word in words:
        word = ''.join(c for c in word if c.isalpha())

        if word in dictionary:
            score += 1

    return score


def dictionary_attack(ciphertext, dictionary_file):
    dictionary = load_dictionary(dictionary_file)

    best_key = 0
    best_plaintext = ""
    best_score = -1

    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = dictionary_score(plaintext, dictionary)

        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score


if __name__ == "__main__":

    ciphertext = "WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ"

    dictionary_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "dictionary",
        "english_words.txt"
    )

    key, plaintext, score = dictionary_attack(
        ciphertext,
        dictionary_file
    )

    print("Ciphertext:", ciphertext)
    print("Predicted Key:", key)
    print("Plaintext:", plaintext)
    print("Dictionary Score:", score)