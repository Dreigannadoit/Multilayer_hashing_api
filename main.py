from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api import router
from modules.Rot_Cryp import ROT32Cipher
from modules.Vige_Cryp import VigenereCipher

app = FastAPI(
    title="Encryption Visualizer API",
    description="API for visualizing encryption transformations",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def welcome():
    return {
        "message": "Welcome to Encryption Visualizer API",
        "endpoints": {
            "encrypt_rot32": "/api/encrypt/rot32",
            "decrypt_rot32": "/api/decrypt/rot32",
            "encrypt_vigenere": "/api/encrypt/vigenere",
            "decrypt_vigenere": "/api/decrypt/vigenere"
        }
    }

def run_on_terminal():
    rot = ROT32Cipher()
    vig = VigenereCipher()

    mode = input(
        "Choose mode (1-ROT32 Encrypt, 2-ROT32 Decrypt, "
        "3-Vigenere Encrypt, 4-Vigenere Decrypt): "
    )

    if mode == "1":
        m = input("Enter a plaintext: ")
        print("Encrypted Text:", rot.encrypt(m))

    elif mode == "2":
        c = input("Enter a ciphertext: ")
        print("Decrypted Text:", rot.decrypt(c))

    elif mode == "3":
        m = input("Enter a plaintext: ")
        k = input("Enter a key: ")
        print("Encrypted Text:", vig.encrypt(m, k))

    elif mode == "4":
        c = input("Enter a ciphertext: ")
        k = input("Enter a key: ")
        print("Decrypted Text:", vig.decrypt(c, k))

    else:
        print("Invalid choice")

if __name__ == "__main__":
    run_on_terminal()
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)