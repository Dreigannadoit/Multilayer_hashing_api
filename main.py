from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api import router

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)