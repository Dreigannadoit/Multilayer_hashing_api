from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from modules.Rot_Cryp import ROT32Cipher
from modules.Vige_Cryp import VigenereCipher
from utils.utils import char_to_ascii_bits, bits_to_base64, base64_to_bits, ascii_bits_to_char

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
            step="original",
            data=request.plaintext,
            description="Original plaintext input"
        ))
        
        # Step 2: Convert to ASCII bits
        bits = char_to_ascii_bits(request.plaintext)
        steps.append(TransformationStep(
            step="ascii_bits",
            data=bits[:50] + "..." if len(bits) > 50 else bits,
            description="Converted to ASCII bits (8 bits per character)"
        ))
        
        # Step 3: Convert to Base64
        b64 = bits_to_base64(bits)
        steps.append(TransformationStep(
            step="base64",
            data=b64,
            description="Converted bits to Base64"
        ))
        
        # Step 4: Apply ROT32
        result = rot_cipher.encrypt(request.plaintext)
        steps.append(TransformationStep(
            step="rot32_encrypted",
            data=result,
            description="Applied ROT32 encryption to Base64"
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
            step="encrypted_input",
            data=request.ciphertext,
            description="Received encrypted text"
        ))
        
        # Step 2: Apply ROT32 decryption
        b64 = rot_cipher._rot_decrypt(request.ciphertext)
        steps.append(TransformationStep(
            step="base64_after_rot",
            data=b64,
            description="Applied ROT32 decryption to get Base64"
        ))
        
        # Step 3: Convert Base64 to bits
        bits = base64_to_bits(b64)
        steps.append(TransformationStep(
            step="bits_after_base64",
            data=bits[:50] + "..." if len(bits) > 50 else bits,
            description="Converted Base64 back to bits"
        ))
        
        # Step 4: Convert bits to text
        result = ascii_bits_to_char(bits)
        steps.append(TransformationStep(
            step="decrypted_text",
            data=result,
            description="Converted bits to final text"
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
            step="original",
            data=f"Plaintext: {request.plaintext}\nKey: {request.key}",
            description="Original input with encryption key"
        ))
        
        # Step 2: Convert plaintext to bits
        m_bits = char_to_ascii_bits(request.plaintext)
        steps.append(TransformationStep(
            step="plaintext_bits",
            data=m_bits[:50] + "..." if len(m_bits) > 50 else m_bits,
            description="Plaintext converted to ASCII bits"
        ))
        
        # Step 3: Convert key to bits
        k_bits = char_to_ascii_bits(request.key)
        steps.append(TransformationStep(
            step="key_bits",
            data=k_bits[:50] + "..." if len(k_bits) > 50 else k_bits,
            description="Key converted to ASCII bits"
        ))
        
        # Step 4: Convert to Base64 (remove padding)
        m_b64 = bits_to_base64(m_bits).replace("=", "")
        k_b64 = bits_to_base64(k_bits).replace("=", "")
        steps.append(TransformationStep(
            step="base64_conversion",
            data=f"Plaintext Base64: {m_b64}\nKey Base64: {k_b64}",
            description="Converted bits to Base64 (padding removed)"
        ))
        
        # Step 5: Apply Vigenere encryption
        result = vigenere_cipher.encrypt(request.plaintext, request.key)
        steps.append(TransformationStep(
            step="vigenere_encrypted",
            data=result,
            description="Applied Vigenere encryption to Base64"
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
            step="encrypted_input",
            data=f"Ciphertext: {request.ciphertext}\nKey: {request.key}",
            description="Received encrypted text with decryption key"
        ))
        
        # Step 2: Convert key to bits
        k_bits = char_to_ascii_bits(request.key)
        steps.append(TransformationStep(
            step="key_bits",
            data=k_bits[:50] + "..." if len(k_bits) > 50 else k_bits,
            description="Key converted to ASCII bits"
        ))
        
        # Step 3: Convert key to Base64
        k_b64 = bits_to_base64(k_bits).replace("=", "")
        steps.append(TransformationStep(
            step="key_base64",
            data=k_b64,
            description="Key converted to Base64"
        ))
        
        # Step 4: Apply Vigenere decryption
        m_b64 = vigenere_cipher._decrypt_base64(request.ciphertext, k_b64)
        steps.append(TransformationStep(
            step="base64_after_vigenere",
            data=m_b64,
            description="Applied Vigenere decryption to get Base64"
        ))
        
        # Step 5: Decrypt to get result
        result = vigenere_cipher.decrypt(request.ciphertext, request.key)
        steps.append(TransformationStep(
            step="decrypted_text",
            data=result,
            description="Converted Base64 to final text"
        ))
        
        return DecryptResponse(result=result, steps=steps)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))