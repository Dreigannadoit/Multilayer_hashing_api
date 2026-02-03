ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def char_to_ascii_bits(s):
    return ''.join(f"{ord(c):08b}" for c in s)

def ascii_bits_to_char(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def base64_to_bits(b64):
    bits = ""
    for c in b64:
        if c != '=':
            bits += f"{ALPHABET.index(c):06b}"
    return bits

def repeat_key(key, length):
    return (key * (length // len(key) + 1))[:length]
