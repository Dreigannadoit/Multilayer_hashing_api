from modules.Rot_Cryp import ROT32Cipher
from modules.Vige_Cryp import VigenereCipher

def run():
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
    run()
    # pass
