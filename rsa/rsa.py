import math
import string
import argparse

from sympy import mod_inverse

ALPHABET: str = string.ascii_uppercase + "_"
ALPHABET_LEN: int = len(ALPHABET)

ENCRYPT_BLOCK_SIZE: int = 2
DECRYPT_BLOCK_SIZE: int = 3


def prepare_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RSA Encryptor/Decryptor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a message using RSA")
    encrypt_parser.add_argument("p", type=int, help="First prime number")
    encrypt_parser.add_argument("q", type=int, help="Second prime number")
    encrypt_parser.add_argument("text", type=str, help="Text to encrypt")

    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a message using RSA")
    decrypt_parser.add_argument("p", type=int, help="First prime number")
    decrypt_parser.add_argument("q", type=int, help="Second prime number")
    decrypt_parser.add_argument("chipertext", type=str, help="Chipertext to decrypt")

    return parser


class Encryptor(object):
    def __init__(self) -> None:
        pass

    def _letters_to_num(self, letters: str) -> int:
        num = 0
        for letter in letters:
            if letter == "_":
                num *= ALPHABET_LEN
            else:
                num = num * ALPHABET_LEN + (ord(letter) - (ord(ALPHABET[0]) - 1))
        return num

    def _num_to_letters(self, num: int) -> str:
        text = ""
        for i in range(2, -1, -1):
            coeff = num // (ALPHABET_LEN**i)
            num %= ALPHABET_LEN**i

            if coeff > 0:
                text += chr(coeff + (ord(ALPHABET[0]) - 1))
            else:
                text += "_"
        return text

    def encrypt(self, p: int, q: int, text: str) -> str:
        n = p * q
        phi_n = (p - 1) * (q - 1)

        e = 2
        while True:
            if phi_n > e > 1 == math.gcd(e, phi_n):
                break
            e += 1

        text = text.upper()
        text_blocks = [text[i : i + ENCRYPT_BLOCK_SIZE] for i in range(0, len(text), ENCRYPT_BLOCK_SIZE)]

        numerical_blocks = [self._letters_to_num(block) for block in text_blocks]
        encrypted_numerical_blocks = [pow(block, e, n) for block in numerical_blocks]

        encrypted_letters_blocks = [self._num_to_letters(num) for num in encrypted_numerical_blocks]
        chipertext = "".join(encrypted_letters_blocks)

        print("Values:\n")
        print("##############################")
        print(f"\nn = {n} | phi(n) = {phi_n} | e = {e}\n")
        print("##############################")

        print("\nPlaintext:\n")
        for i, block in enumerate(text_blocks):
            print(
                f"Block {i+1} of {ENCRYPT_BLOCK_SIZE} letters: {block} | Numerical equivalent: {numerical_blocks[i]}"
            )

        print(f"\nEncryption:\n")
        for i, (num_block, letter_block) in enumerate(zip(encrypted_numerical_blocks, encrypted_letters_blocks)):
            print(f"c{i+1} = b{i+1}^e mod n = {num_block} | Block of {ENCRYPT_BLOCK_SIZE} letters: {letter_block}")

        print(f"\nChipertext: {chipertext}\n")
        return chipertext


class Decryptor(object):
    def __init__(self) -> None:
        pass

    def _letters_to_num(self, letters: str) -> int:
        num = 0

        for i, letter in enumerate(reversed(letters)):
            if letter == "_":
                coeff = 0
            else:
                coeff = ord(letter.upper()) - ord(ALPHABET[0]) + 1
            num += coeff * (ALPHABET_LEN**i)
        return num

    def _num_to_letters(self, num: int) -> str:
        text = ""
        while num > 0:
            num, rem = divmod(num, ALPHABET_LEN)
            if rem == 0:
                text = "_" + text
            else:
                text = chr((ord(ALPHABET[0]) - 1) + rem) + text
        return text.rjust(ENCRYPT_BLOCK_SIZE, "_")

    def decrypt(self, p: int, q: int, chipertext: str) -> str:
        n = p * q
        phi_n = (p - 1) * (q - 1)

        e = 2
        while True:
            if phi_n > e > 1 == math.gcd(e, phi_n):
                break
            e += 1

        d = mod_inverse(e, phi_n)

        chipertext = chipertext.upper()
        chipertext_blocks = [
            chipertext[i : i + DECRYPT_BLOCK_SIZE] for i in range(0, len(chipertext), DECRYPT_BLOCK_SIZE)
        ]

        numerical_blocks = [self._letters_to_num(block) for block in chipertext_blocks]
        decrypted_numerical_blocks = [pow(block, d, n) for block in numerical_blocks]

        decrypted_letters_blocks = [self._num_to_letters(num) for num in decrypted_numerical_blocks]
        plaintext = "".join(decrypted_letters_blocks)

        print("Values:\n")
        print("##############################")
        print(f"\nn = {n} | phi(n) = {phi_n} | e = {e} | d = {d}\n")
        print("##############################")

        print("\nChipertext:\n")
        for i, block in enumerate(chipertext_blocks):
            print(
                f"Block {i+1} of {DECRYPT_BLOCK_SIZE} letters: {block} | Numerical equivalent: {numerical_blocks[i]}"
            )

        print(f"\nDecryption:\n")
        for i, (num_block, letter_block) in enumerate(zip(decrypted_numerical_blocks, decrypted_letters_blocks)):
            print(f"b{i+1} = c{i+1}^d mod n = {num_block} | Block of {ENCRYPT_BLOCK_SIZE} letters: {letter_block}")

        print(f"\nPlaintext: {plaintext}\n")
        return plaintext


if __name__ == "__main__":
    parser = prepare_parser()

    args = parser.parse_args()
    match args.command:
        case "encrypt":
            encryptor = Encryptor()
            encryptor.encrypt(args.p, args.q, args.text)
        case "decrypt":
            decryptor = Decryptor()
            decryptor.decrypt(args.p, args.q, args.chipertext)
        case _:
            parser.print_help()
            exit(1)
