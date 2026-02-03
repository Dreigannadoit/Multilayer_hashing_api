from utils.utils import (
    ALPHABET,
    char_to_ascii_bits,
    ascii_bits_to_char,
    bits_to_base64,
    base64_to_bits
)

class ROT32Cipher:

    @staticmethod
    def _rot_encrypt(b64):
        return ''.join(
            ALPHABET[(ALPHABET.index(c) + 32) % 64] if c != '=' else '='
            for c in b64
        )

    @staticmethod
    def _rot_decrypt(b64):
        return ''.join(
            ALPHABET[(ALPHABET.index(c) - 32) % 64] if c != '=' else '='
            for c in b64
        )

    def encrypt(self, plaintext):
        bits = char_to_ascii_bits(plaintext)
        b64 = bits_to_base64(bits)
        return self._rot_encrypt(b64)

    def decrypt(self, ciphertext):
        b64 = self._rot_decrypt(ciphertext)
        bits = base64_to_bits(b64)
        return ascii_bits_to_char(bits)
