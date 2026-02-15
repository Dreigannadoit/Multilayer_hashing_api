from utils.utils import (
    ALPHABET,
    char_to_ascii_bits,
    ascii_bits_to_char,
    bits_to_base64,
    base64_to_bits,
    repeat_key
)

class VigenereCipher:

    @staticmethod
    def _encrypt_base64(m, k):
        result = ""
        for mc, kc in zip(m, k):
            mi = ALPHABET.index(mc)
            ki = ALPHABET.index(kc)
            result += ALPHABET[(mi + ki) % 64]
        return result

    @staticmethod
    def _decrypt_base64(c, k):
        result = ""
        for cc, kc in zip(c, k):
            ci = ALPHABET.index(cc)
            ki = ALPHABET.index(kc)
            result += ALPHABET[(ci - ki) % 64]
        return result

    def encrypt(self, plaintext, key):
        # Convert plaintext to ASCII bits -> Convert plaintext bits to Base64 -> Convert key to ASCII bits -> Convert key bits to Base64 -> Repeat key to match plaintext length -> Apply Vigenere encryption
        m_bits = char_to_ascii_bits(plaintext)
        m_b64 = bits_to_base64(m_bits)
        m_b64 = m_b64.rstrip('=')
        k_bits = char_to_ascii_bits(key)
        k_b64 = bits_to_base64(k_bits)
        k_b64 = k_b64.rstrip('=')
        k_b64 = repeat_key(k_b64, len(m_b64))
        return self._encrypt_base64(m_b64, k_b64)

    def decrypt(self, ciphertext, key):
        # Convert key to ASCII bits -> Convert key bits to Base64 -> Repeat key to match ciphertext length -> Apply Vigenere decryption -> Convert Base64 to bits -> Convert bits to text
        k_bits = char_to_ascii_bits(key)
        k_b64 = bits_to_base64(k_bits)
        k_b64 = k_b64.rstrip('=')
        k_b64 = repeat_key(k_b64, len(ciphertext))
        m_b64 = self._decrypt_base64(ciphertext, k_b64)
        bits = base64_to_bits(m_b64)
        return ascii_bits_to_char(bits)