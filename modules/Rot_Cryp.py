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
        result = ""
        for c in b64:
            if c == '=':
                result += '='
            else:
                idx = ALPHABET.index(c)
                new_idx = (idx + 32) % 64
                result += ALPHABET[new_idx]
        return result

    @staticmethod
    def _rot_decrypt(b64):
        result = ""
        for c in b64:
            if c == '=':
                result += '='
            else:
                idx = ALPHABET.index(c)
                new_idx = (idx - 32) % 64
                result += ALPHABET[new_idx]
        return result

    def encrypt(self, plaintext):
        # Process: ASCII bits -> Step 2: Group into 6 bits and convert to Base64 -> Step 3: Apply ROT32 rotation
        bits = char_to_ascii_bits(plaintext)
        b64 = bits_to_base64(bits)
        return self._rot_encrypt(b64)

    def decrypt(self, ciphertext):
        # Apply ROT32 decryption -> Convert Base64 to bits -> Group into 8 bits and convert to text
        b64 = self._rot_decrypt(ciphertext)
        bits = base64_to_bits(b64)
        return ascii_bits_to_char(bits)