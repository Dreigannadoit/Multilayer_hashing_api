# Data Obfuscation - MultiLayer Hashing Algorithm

Data obfuscation (DO) is a technique that masks data by scrambling it to prevent unauthorized access to sensitive information. In particular, we perform cryptographic data obfuscation, which involves encoding data before it is transferred to another encryption scheme. This will remove the ability to use frequency analysis to break ciphers.

Read the following topics in Obfuscating Data ([click here](https://online.msuiit.edu.ph/moodle/mod/resource/view.php?id=180166) for the reading material)

- ASCII Encoding
- Base64 Encoding Text
- Binary Data
- Decoding

----


### Sample Input, Process, and Output

#### For encryption:
1. User enters plaintext message m ∈ M = {A-Z, a-z, 0-9}^n 
2. m is converted to a binary string using ASCII: mASCII ∈ {0, 1}^8n 
3. mASCII is grouped into 6 bits
4. Each 6-bit group is converted to Base64 (see table below), mBase64 = {A-Z, a-z, 0-9, +, /}^n/6
5. For each Base64 character in m (Base64):
    - If the cipher involves letter rotation, rotate 32 characters after it
    - Else if the cipher involves a key (i.e., Vigenere cipher)
	    - Repeat steps 2-4 for the key; the resulting key becomes k (Base64)
	    - Perform character addition (c (Base64) = m (Base64) + k (Base64)) based on index

    - In each of the cases 5.A and 5.B, the result is c (Base64)
6. Encrypted output is displayed as the ciphertext

#### For decryption:
1. User enters a Base64 encoded ciphertext cBase64 ∈ C = {A-Z, a-z, 0-9, +, /}^n/6 
2. For each Base64 character in cBase64:
    - If the cipher involves letter rotation, rotate 32 characters before it
    - Else if the cipher involves a key (i.e., Vigenere cipher), perform character subtraction (m (Base64) = c (Base64) - k (Base64)) based on index
    - In each of the cases 2.A and 2.B, the result is m (Base64)

3. m (Base64) is converted to a binary string: m (Base64) ∈ {0, 1}^6n+p 
4. m (Base64) is grouped into 8 bits, which becomes mASCII ∈ {0, 1}^8n 
5. Each 8-bit group is converted to its ASCII character representation
6. The decrypted text m is displayed, m ∈ {A-Z, a-z, 0-9}^n
---
### How to Use
##### Making Alphabete Table
In the Main folder create a `.env` file. In it, define your alphabete as `ALPHABET_TABLE`
```.env
ALPHABET_TABLE="qwertyuiopasdfghjklzxcvbnm{}:"<>?"
```
