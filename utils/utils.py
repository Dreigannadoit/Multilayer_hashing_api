import os
import base64
from dotenv import load_dotenv

load_dotenv()

ALPHABET = os.getenv("ALPHABET_TABLE")

# Ensure ALPHABET has all 64 characters
if len(ALPHABET) != 64:
    print(f"Warning: ALPHABET has {len(ALPHABET)} characters, should be 64")
    # If missing + and /, add them
    if '+' not in ALPHABET:
        ALPHABET += '+'
    if '/' not in ALPHABET:
        ALPHABET += '/'

def char_to_ascii_bits(s):
    return ''.join(f"{ord(c):08b}" for c in s)

def ascii_bits_to_char(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def bits_to_base64(bits):
    bytes_data = bits_to_bytes(bits)
    base64_bytes = base64.b64encode(bytes_data)
    return base64_bytes.decode('utf-8')

def base64_to_bits(b64):
    decoded_bytes = base64.b64decode(b64)
    return bytes_to_bits(decoded_bytes)

def bits_to_bytes(bits):
    padding = (8 - len(bits) % 8) % 8
    bits_padded = bits + '0' * padding
    
    bytes_list = []
    for i in range(0, len(bits_padded), 8):
        byte_bits = bits_padded[i:i+8]
        bytes_list.append(int(byte_bits, 2))
    
    return bytes(bytes_list)

def bytes_to_bits(bytes_data):
    return ''.join(f"{byte:08b}" for byte in bytes_data)

def repeat_key(key, length):
    return (key * (length // len(key) + 1))[:length]

def validate_base64_string(s):
    """Validate that all characters in string are in the Base64 alphabet"""
    invalid_chars = [c for c in s if c not in ALPHABET and c != '=']
    if invalid_chars:
        raise ValueError(f"Invalid Base64 characters: {invalid_chars}")
    return True

if __name__ == "__main__":
    # Simple test
    text = "Hello World!"
    bits = char_to_ascii_bits(text)
    print(f"Original: {text}")
    print(f"Bits: {bits[:50]}...")
    
    # Convert to Base64
    b64 = bits_to_base64(bits)
    print(f"Base64: {b64}")
    print(f"Base64 length: {len(b64)}")
    print(f"ALPHABET length: {len(ALPHABET)}")
    print(f"ALPHABET: {ALPHABET}")
    
    # Test each character in b64 is in ALPHABET (except '=')
    for c in b64:
        if c != '=' and c not in ALPHABET:
            print(f"WARNING: '{c}' not in ALPHABET!")
    
    # Convert back
    recovered_bits = base64_to_bits(b64)
    recovered_text = ascii_bits_to_char(recovered_bits)
    print(f"Recovered: {recovered_text}")
    
    # Test repeat_key
    print(f"\nrepeat_key('KEY', 10): {repeat_key('KEY', 10)}")