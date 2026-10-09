BLOCK_SIZE = 16


def recover_plaintext(iv, ciphertext, oracle):
    """
    Recover plaintext using a padding oracle.
    The AES key is never provided to this function.
    """
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV must be 16 bytes")

    if not ciphertext or len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Invalid ciphertext length")

    blocks = [
        ciphertext[i:i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    recovered = bytearray()
    previous = iv

    for block in blocks:
        intermediate = bytearray(BLOCK_SIZE)
        plaintext_block = bytearray(BLOCK_SIZE)

        for pad_value in range(1, BLOCK_SIZE + 1):
            position = BLOCK_SIZE - pad_value
            crafted = bytearray(BLOCK_SIZE)

            # Force already recovered bytes to have valid padding.
            for j in range(position + 1, BLOCK_SIZE):
                crafted[j] = intermediate[j] ^ pad_value

            found = False

            for guess in range(256):
                crafted[position] = guess

                if oracle(bytes(crafted), block):
                    # Check for accidental valid padding when
                    # recovering the final byte.
                    if pad_value == 1 and position > 0:
                        check = bytearray(crafted)
                        check[position - 1] ^= 1

                        if not oracle(bytes(check), block):
                            continue

                    intermediate[position] = guess ^ pad_value
                    plaintext_block[position] = (
                        intermediate[position] ^ previous[position]
                    )

                    found = True
                    break

            if not found:
                raise ValueError(
                    f"Recovery failed at byte position {position}"
                )

        recovered.extend(plaintext_block)
        previous = block

    # Remove PKCS#7 padding.
    pad_value = recovered[-1]

    if not 1 <= pad_value <= BLOCK_SIZE:
        raise ValueError("Invalid recovered padding")

    if recovered[-pad_value:] != bytes([pad_value]) * pad_value:
        raise ValueError("Invalid recovered padding")

    return bytes(recovered[:-pad_value])
