from cryptanalysis import (
    add_mapping,
    apply_partial_substitution,
    display_mapping,
    is_valid_mapping
)


mapping = {}

print("Adding C -> T:")
print(add_mapping(mapping, "C", "T"))

print("Adding X -> H:")
print(add_mapping(mapping, "X", "H"))

print("Adding C -> T again:")
print(add_mapping(mapping, "C", "T"))

print("Trying X -> T:")
print(add_mapping(mapping, "X", "T"))

print()

ciphertext = "CX XQ CXX."

partial = apply_partial_substitution(
    ciphertext,
    mapping
)

print("Ciphertext:")
print(ciphertext)

print("\nPartial plaintext:")
print(partial)

print()

display_mapping(mapping)

print("\nMapping valid:", is_valid_mapping(mapping))