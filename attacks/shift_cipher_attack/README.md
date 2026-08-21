# Shift Cipher Cryptanalysis

## Purpose
Cryptanalysis of a Shift Cipher using brute force, dictionary scoring, and Chi-Square analysis.

## Algorithms
- `src/shift_cipher.py`: Shift Cipher encryption/decryption and 26-key brute force.
- `src/brute_force_dictionary.py`: scores each candidate plaintext using an English dictionary.
- `src/chi_square_attack.py`: compares candidate letter distributions against standard English frequencies.
- `src/main.py`: runs both attacks and records experimental results.

## Run
From `attacks/shift_cipher_attack`:

```bash
python3 src/main.py --text "KHOOR ZRUOG" --actual-key 3
```

## Experimental test cases
The test cases are stored in `testcases/testcases.csv`. The supplied dictionary is intentionally compact for a laboratory demonstration; a larger English corpus can improve dictionary scoring.
