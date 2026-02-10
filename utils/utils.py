import os
import base64
from dotenv import load_dotenv

load_dotenv()

ALPHABET = os.getenv("ALPHABET_TABLE")

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



if __name__ == "__main__":
    # Simple test
    text = "Hello World!"
    bits = char_to_ascii_bits(text)
    print(f"Original: {text}")
    print(f"Bits: {bits[:50]}...")
    
    # Convert to Base64
    b64 = bits_to_base64(bits)
    print(f"Base64: {b64}")
    
    # Convert back
    recovered_bits = base64_to_bits(b64)
    recovered_text = ascii_bits_to_char(recovered_bits)
    print(f"Recovered: {recovered_text}")
    
    # Test repeat_key
    print(f"\nrepeat_key('KEY', 10): {repeat_key('KEY', 10)}")