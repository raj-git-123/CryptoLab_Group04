from pathlib import Path
import argparse
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(Path(__file__).resolve().parent))
from shift_cipher import encrypt
from brute_force_dictionary import dictionary_attack
from chi_square_attack import chi_square_attack


def main():
    parser = argparse.ArgumentParser(description='Shift Cipher cryptanalysis')
    parser.add_argument('--text', required=True, help='Ciphertext to attack')
    parser.add_argument('--actual-key', type=int, default=None, help='Known key for experiment comparison')
    parser.add_argument('--dictionary', default=str(ROOT / 'dictionary' / 'english_words.txt'))
    parser.add_argument('--output', default=str(ROOT / 'outputs' / 'results.csv'))
    args = parser.parse_args()

    dictionary_results = dictionary_attack(args.text, args.dictionary)
    chi_results = chi_square_attack(args.text)

    d_score, d_key, d_plain = dictionary_results[0]
    c_score, c_key, c_plain = chi_results[0]

    print('\nDictionary scoring:')
    print(f'Predicted key : {d_key}')
    print(f'Score         : {d_score}')
    print(f'Plaintext     : {d_plain}')

    print('\nChi-Square analysis:')
    print(f'Predicted key : {c_key}')
    print(f'Chi-Square    : {c_score:.4f}')
    print(f'Plaintext     : {c_plain}')

    if args.actual_key is not None:
        print('\nComparison:')
        print(f'Actual key            : {args.actual_key % 26}')
        print(f'Dictionary correct    : {d_key == args.actual_key % 26}')
        print(f'Chi-Square correct    : {c_key == args.actual_key % 26}')

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    write_header = not out.exists()
    with out.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(['Ciphertext', 'Actual Key', 'Dictionary Key', 'Chi-Square Key', 'Dictionary Correct', 'Chi-Square Correct', 'Dictionary Plaintext', 'Chi-Square Plaintext'])
        writer.writerow([args.text, '' if args.actual_key is None else args.actual_key % 26,
                         d_key, c_key, d_key == (args.actual_key % 26 if args.actual_key is not None else d_key),
                         c_key == (args.actual_key % 26 if args.actual_key is not None else c_key), d_plain, c_plain])


if __name__ == '__main__':
    main()
