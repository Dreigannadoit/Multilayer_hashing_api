from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from modules.Rot_Cryp import ROT32Cipher
from modules.Vige_Cryp import VigenereCipher
from utils.utils import ALPHABET, char_to_ascii_bits, bits_to_base64, base64_to_bits, ascii_bits_to_char, repeat_key

# Initialize ciphers
rot_cipher = ROT32Cipher()
vigenere_cipher = VigenereCipher()

router = APIRouter()

# Request/Response models
class EncryptRequest(BaseModel):
    plaintext: str
    key: Optional[str] = None

class DecryptRequest(BaseModel):
    ciphertext: str
    key: Optional[str] = None

class TransformationStep(BaseModel):
    step: str
    data: str
    description: str

class EncryptResponse(BaseModel):
    result: str
    steps: List[TransformationStep]

class DecryptResponse(BaseModel):
    result: str
    steps: List[TransformationStep]

@router.get("/")
async def root():
    return {"message": "Encryption Visualizer API"}

@router.post("/encrypt/rot32", response_model=EncryptResponse)
async def encrypt_rot32(request: EncryptRequest):
    try:
        steps = []
        
        # Step 1: Original text
        steps.append(TransformationStep(
            step="original text",
            data=request.plaintext,
            description="Original plaintext input"
        ))
        
        # Step 2: Convert to ASCII bits (8-bit groups)
        bits = char_to_ascii_bits(request.plaintext)
        # Format as 8-bit groups for display
        formatted_bits = ' '.join([bits[i:i+8] for i in range(0, len(bits), 8)])
        steps.append(TransformationStep(
            step="ASCII bits (8-bit groups)",
            data=formatted_bits,
            description="Each character converted to 8-bit ASCII"
        ))
        
        # Step 3: Show 6-bit grouping (visualization only)
        # Pad bits to make length divisible by 6
        padding_needed = (6 - len(bits) % 6) % 6
        padded_bits = bits + '0' * padding_needed
        
        six_bit_groups = [padded_bits[i:i+6] for i in range(0, len(padded_bits), 6)]
        six_bit_display = ' '.join(six_bit_groups)
        steps.append(TransformationStep(
            step="6-bit groups",
            data=six_bit_display,
            description=f"Bits grouped into 6-bit chunks (added {padding_needed} padding bits)"
        ))
        
        # Step 4: Convert to Base64 (using your existing function)
        b64 = bits_to_base64(bits)
        
        # Show mapping of 6-bit groups to Base64 chars
        mapping_display = ""
        base64_chars = list(b64)
        for i, (group, char) in enumerate(zip(six_bit_groups[:len(base64_chars)], base64_chars)):
            if char != '=':
                idx = ALPHABET.index(char)
                mapping_display += f"Group {i+1}: {group} → '{char}' (index {idx})\n"
            else:
                mapping_display += f"Group {i+1}: {group} → '{char}' (padding)\n"
        
        steps.append(TransformationStep(
            step="Base64 encoding",
            data=f"Base64: {b64}\n\nMapping:\n{mapping_display}",
            description="Each 6-bit group mapped to Base64 character"
        ))
        
        # Step 5: Apply ROT32 (using your existing function)
        result = rot_cipher.encrypt(request.plaintext)
        
        # Show ROT32 transformation
        rot_display = ""
        for i, (orig_char, new_char) in enumerate(zip(b64, result)):
            if orig_char != '=':
                orig_idx = ALPHABET.index(orig_char)
                new_idx = (orig_idx + 32) % 64
                rot_display += f"'{orig_char}' (index {orig_idx:2d}) → +32 → '{new_char}' (index {new_idx:2d})\n"
            else:
                rot_display += f"'{orig_char}' (padding) → '{new_char}'\n"
        
        steps.append(TransformationStep(
            step="ROT32 rotation",
            data=f"Ciphertext: {result}\n\nRotation details:\n{rot_display}",
            description="Each Base64 character rotated by 32 positions"
        ))
        
        return EncryptResponse(result=result, steps=steps)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/decrypt/rot32", response_model=DecryptResponse)
async def decrypt_rot32(request: DecryptRequest):
    try:
        steps = []
        
        # Step 1: Encrypted input
        steps.append(TransformationStep(
            step="ciphertext input",
            data=request.ciphertext,
            description="Received encrypted text"
        ))
        
        # Step 2: Apply ROT32 decryption
        b64 = rot_cipher._rot_decrypt(request.ciphertext)
        
        # Show ROT32 decryption
        rot_display = ""
        for i, (cipher_char, base64_char) in enumerate(zip(request.ciphertext, b64)):
            if cipher_char != '=':
                cipher_idx = ALPHABET.index(cipher_char)
                base64_idx = (cipher_idx - 32) % 64
                rot_display += f"'{cipher_char}' (index {cipher_idx:2d}) → -32 → '{base64_char}' (index {base64_idx:2d})\n"
            else:
                rot_display += f"'{cipher_char}' (padding) → '{base64_char}'\n"
        
        steps.append(TransformationStep(
            step="ROT32 decryption",
            data=f"Base64: {b64}\n\nRotation details:\n{rot_display}",
            description="Applied ROT32 decryption to get Base64"
        ))
        
        # DEBUG: Show what base64_to_bits is doing
        debug_bits = base64_to_bits(b64)
        steps.append(TransformationStep(
            step="DEBUG - raw bits from base64_to_bits",
            data=debug_bits,
            description="Raw bits output from base64_to_bits()"
        ))
        
        # Show the 6-bit groups from Base64
        bits_from_b64 = base64_to_bits(b64)
        
        # Show the 6-bit groups from Base64
        six_bit_groups = []
        temp_bits = bits_from_b64
        for i in range(0, len(temp_bits), 6):
            if i+6 <= len(temp_bits):
                six_bit_groups.append(temp_bits[i:i+6])
        
        six_bit_display = ' '.join(six_bit_groups)
        steps.append(TransformationStep(
            step="6-bit groups from Base64",
            data=six_bit_display,
            description="Base64 decoded back to 6-bit groups"
        ))
        
        # Group into 8-bit ASCII
        eight_bit_groups = []
        for i in range(0, len(bits_from_b64), 8):
            if i+8 <= len(bits_from_b64):
                eight_bit_groups.append(bits_from_b64[i:i+8])
        
        eight_bit_display = ' '.join(eight_bit_groups)
        steps.append(TransformationStep(
            step="8-bit ASCII groups",
            data=eight_bit_display,
            description="6-bit groups recombined into 8-bit ASCII groups"
        ))
        
        # Convert to text
        result = rot_cipher.decrypt(request.ciphertext)
        steps.append(TransformationStep(
            step="ASCII to text",
            data=result,
            description="8-bit groups converted back to characters"
        ))
        
        return DecryptResponse(result=result, steps=steps)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/encrypt/vigenere", response_model=EncryptResponse)
async def encrypt_vigenere(request: EncryptRequest):
    if not request.key:
        raise HTTPException(status_code=400, detail="Key is required for Vigenere cipher")
    
    try:
        steps = []
        
        # Step 1: Original text and key
        steps.append(TransformationStep(
            step="original input",
            data=f"Plaintext: {request.plaintext}\nKey: {request.key}",
            description="Original input with encryption key"
        ))
        
        # Step 2: Convert plaintext to ASCII bits
        m_bits = char_to_ascii_bits(request.plaintext)
        m_bits_formatted = ' '.join([m_bits[i:i+8] for i in range(0, len(m_bits), 8)])
        steps.append(TransformationStep(
            step="plaintext ASCII bits",
            data=m_bits_formatted,
            description="Plaintext converted to 8-bit ASCII"
        ))
        
        # Step 3: Convert key to ASCII bits
        k_bits = char_to_ascii_bits(request.key)
        k_bits_formatted = ' '.join([k_bits[i:i+8] for i in range(0, len(k_bits), 8)])
        steps.append(TransformationStep(
            step="key ASCII bits",
            data=k_bits_formatted,
            description="Key converted to 8-bit ASCII"
        ))
        
        # Step 4: Convert plaintext to Base64
        m_b64_full = bits_to_base64(m_bits)
        m_b64 = m_b64_full.replace("=", "")  # Your module removes padding
        steps.append(TransformationStep(
            step="plaintext Base64",
            data=f"Full Base64 (with padding): {m_b64_full}\nBase64 (padding removed): {m_b64}",
            description="Plaintext converted to Base64"
        ))
        
        # Step 5: Convert key to Base64
        k_b64_full = bits_to_base64(k_bits)
        k_b64 = k_b64_full.replace("=", "")  # Your module removes padding
        steps.append(TransformationStep(
            step="key Base64",
            data=f"Full Base64 (with padding): {k_b64_full}\nBase64 (padding removed): {k_b64}",
            description="Key converted to Base64"
        ))
        
        # Step 6: Repeat key to match plaintext length
        k_b64_repeated = repeat_key(k_b64, len(m_b64))
        steps.append(TransformationStep(
            step="key repetition",
            data=f"Original key Base64: {k_b64}\nRepeated key: {k_b64_repeated}",
            description=f"Key repeated to match plaintext length ({len(m_b64)} characters)"
        ))
        
        # Step 7: Show Vigenere addition (using your existing function's logic)
        addition_display = ""
        result_chars = []
        
        for i, (m_char, k_char) in enumerate(zip(m_b64, k_b64_repeated)):
            mi = ALPHABET.index(m_char)
            ki = ALPHABET.index(k_char)
            result_idx = (mi + ki) % 64
            result_char = ALPHABET[result_idx]
            result_chars.append(result_char)
            
            addition_display += (
                f"'{m_char}' (idx {mi:2d}) + '{k_char}' (idx {ki:2d}) = {mi + ki:3d} "
                f"mod 64 = {result_idx:2d} → '{result_char}'\n"
            )
        
        # Get actual result from your module
        result = vigenere_cipher.encrypt(request.plaintext, request.key)
        
        steps.append(TransformationStep(
            step="Vigenere addition",
            data=f"Calculation:\n{addition_display}\nResult: {result}",
            description="Character-wise addition modulo 64"
        ))
        
        return EncryptResponse(result=result, steps=steps)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/decrypt/vigenere", response_model=DecryptResponse)
async def decrypt_vigenere(request: DecryptRequest):
    if not request.key:
        raise HTTPException(status_code=400, detail="Key is required for Vigenere cipher")
    
    try:
        steps = []
        
        # Step 1: Encrypted input and key
        steps.append(TransformationStep(
            step="ciphertext input",
            data=f"Ciphertext: {request.ciphertext}\nKey: {request.key}",
            description="Received encrypted text with decryption key"
        ))
        
        # Step 2: Convert key to ASCII bits
        k_bits = char_to_ascii_bits(request.key)
        k_bits_formatted = ' '.join([k_bits[i:i+8] for i in range(0, len(k_bits), 8)])
        steps.append(TransformationStep(
            step="key ASCII bits",
            data=k_bits_formatted,
            description="Key converted to 8-bit ASCII"
        ))
        
        # Step 3: Convert key to Base64
        k_b64_full = bits_to_base64(k_bits)
        k_b64 = k_b64_full.replace("=", "")
        steps.append(TransformationStep(
            step="key Base64",
            data=f"Full Base64 (with padding): {k_b64_full}\nBase64 (padding removed): {k_b64}",
            description="Key converted to Base64"
        ))
        
        # Step 4: Repeat key to match ciphertext length
        k_b64_repeated = repeat_key(k_b64, len(request.ciphertext))
        steps.append(TransformationStep(
            step="key repetition",
            data=f"Original key Base64: {k_b64}\nRepeated key: {k_b64_repeated}",
            description=f"Key repeated to match ciphertext length ({len(request.ciphertext)} characters)"
        ))
        
        # Step 5: Show Vigenere subtraction
        subtraction_display = ""
        m_b64_chars = []
        
        for i, (c_char, k_char) in enumerate(zip(request.ciphertext, k_b64_repeated)):
            ci = ALPHABET.index(c_char)
            ki = ALPHABET.index(k_char)
            result_idx = (ci - ki) % 64
            result_char = ALPHABET[result_idx]
            m_b64_chars.append(result_char)
            
            subtraction_display += (
                f"'{c_char}' (idx {ci:2d}) - '{k_char}' (idx {ki:2d}) = {ci - ki:3d} "
                f"mod 64 = {result_idx:2d} → '{result_char}'\n"
            )
        
        m_b64 = ''.join(m_b64_chars)
        steps.append(TransformationStep(
            step="Vigenere subtraction",
            data=f"Calculation:\n{subtraction_display}\nResult Base64: {m_b64}",
            description="Character-wise subtraction modulo 64"
        ))
        
        # Step 6: Convert Base64 to bits
        bits_from_b64 = base64_to_bits(m_b64)
        
        # Step 7: Show 6-bit groups
        six_bit_groups = [bits_from_b64[i:i+6] for i in range(0, len(bits_from_b64), 6)]
        six_bit_display = ' '.join(six_bit_groups)
        steps.append(TransformationStep(
            step="6-bit groups",
            data=six_bit_display,
            description="Base64 decoded to 6-bit groups"
        ))
        
        # Step 8: Group into 8-bit ASCII
        eight_bit_groups = []
        for i in range(0, len(bits_from_b64), 8):
            if i+8 <= len(bits_from_b64):
                eight_bit_groups.append(bits_from_b64[i:i+8])
        
        eight_bit_display = ' '.join(eight_bit_groups)
        steps.append(TransformationStep(
            step="8-bit ASCII groups",
            data=eight_bit_display,
            description="6-bit groups recombined into 8-bit ASCII groups"
        ))
        
        # Step 9: Convert to text (using your existing function)
        result = vigenere_cipher.decrypt(request.ciphertext, request.key)
        steps.append(TransformationStep(
            step="ASCII to text",
            data=result,
            description="8-bit groups converted back to characters"
        ))
        
        return DecryptResponse(result=result, steps=steps)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))