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
    """Convert string to 8-bit ASCII binary string"""
    return ''.join(f"{ord(c):08b}" for c in s)

def ascii_bits_to_char(bits):
    """Convert 8-bit binary string to characters"""
    chars = []
    # Remove any padding bits that might have been added
    bits = bits[:len(bits) - (len(bits) % 8)]
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def bits_to_base64(bits):
    """Convert binary string to Base64 (following instructor's process)"""
    # First, group into 6-bit chunks
    six_bit_groups = []
    for i in range(0, len(bits), 6):
        group = bits[i:i+6]
        # Pad the last group if needed
        if len(group) < 6:
            group = group.ljust(6, '0')
        six_bit_groups.append(group)
    
    # Convert each 6-bit group to Base64 character
    result = ""
    for group in six_bit_groups:
        index = int(group, 2)
        result += ALPHABET[index]
    
    # Add padding if needed (Base64 standard padding)
    padding = (4 - (len(result) % 4)) % 4
    result += '=' * padding
    
    return result

def base64_to_bits(b64):
    """Convert Base64 to binary string (following instructor's process)"""
    # Remove padding
    b64 = b64.rstrip('=')
    
    # Convert each character to 6-bit value
    bits = ""
    for char in b64:
        if char in ALPHABET:
            index = ALPHABET.index(char)
            bits += f"{index:06b}"
    
    return bits

def bits_to_bytes(bits):
    """Convert binary string to bytes (for compatibility)"""
    padding = (8 - len(bits) % 8) % 8
    bits_padded = bits + '0' * padding
    
    bytes_list = []
    for i in range(0, len(bits_padded), 8):
        byte_bits = bits_padded[i:i+8]
        bytes_list.append(int(byte_bits, 2))
    
    return bytes(bytes_list)

def bytes_to_bits(bytes_data):
    """Convert bytes to binary string (for compatibility)"""
    return ''.join(f"{byte:08b}" for byte in bytes_data)

def repeat_key(key, length):
    """Repeat key to match desired length"""
    return (key * (length // len(key) + 1))[:length]

def validate_base64_string(s):
    """Validate that all characters in string are in the Base64 alphabet"""
    invalid_chars = [c for c in s if c not in ALPHABET and c != '=']
    if invalid_chars:
        raise ValueError(f"Invalid Base64 characters: {invalid_chars}")
    return True

if __name__ == "__main__":
    # Test with instructor's example
    text = "Crypto"
    print(f"Original: {text}")
    
    # Step 1: ASCII bits
    bits = char_to_ascii_bits(text)
    print(f"ASCII bits (8-bit groups): {' '.join([bits[i:i+8] for i in range(0, len(bits), 8)])}")
    
    # Step 2: 6-bit groups
    six_bit_groups = []
    padded_bits = bits
    # Pad to multiple of 6
    if len(padded_bits) % 6 != 0:
        padded_bits = padded_bits.ljust(((len(padded_bits) // 6) + 1) * 6, '0')
    
    for i in range(0, len(padded_bits), 6):
        six_bit_groups.append(padded_bits[i:i+6])
    print(f"6-bit groups: {' '.join(six_bit_groups)}")
    
    # Step 3: Base64
    b64 = bits_to_base64(bits)
    print(f"Base64: {b64}")
    
    # Step 4: Back to bits
    recovered_bits = base64_to_bits(b64)
    print(f"Recovered 6-bit groups: {' '.join([recovered_bits[i:i+6] for i in range(0, len(recovered_bits), 6)])}")
    
    # Step 5: Back to text
    recovered_text = ascii_bits_to_char(recovered_bits)
    print(f"Recovered text: {recovered_text}")