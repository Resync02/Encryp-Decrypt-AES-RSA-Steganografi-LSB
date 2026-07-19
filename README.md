# Multi-Algorithm Encryp-Decrypt

A Python-based implementation of the **ElGamal Cryptosystem** for encrypting and decrypting text files. This project demonstrates the fundamental concepts of asymmetric cryptography using public and private keys, making it suitable for learning and educational purposes.

---

## Features

- Encrypt text files using the ElGamal algorithm.
- Decrypt encrypted files back to their original content.
- Generate public and private key pairs.
- Simple command-line interface.
- Lightweight implementation using pure Python.

---

## Technologies Used

- Python 3.x

---

## Project Structure

```
.
├── elgamal.py          # Main program
├── test1.txt           # Sample plaintext
├── test1_enc.enc       # Encrypted file
├── hasil_enc.txt       # Encryption output
└── README.md           # Documentation
```

---

## How It Works

The application performs the following steps:

1. Generate ElGamal public and private keys.
2. Read plaintext from a text file.
3. Encrypt the plaintext using the recipient's public key.
4. Save the encrypted result into a file.
5. Decrypt the encrypted file using the private key.
6. Display or save the recovered plaintext.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Resync02/ELGAMAL-Encrypt-Decrypt.git
```

Navigate to the project directory:

```bash
cd ELGAMAL-Encrypt-Decrypt
```

---

## Usage

Run the program:

```bash
python elgamal.py
```

Follow the on-screen instructions to:

- Generate keys
- Encrypt a text file
- Decrypt an encrypted file

---

## Example Workflow

**Plaintext**

```
Hello, World!
```

↓

**Encrypted Output**

```
(23456, 78901)
(54321, 12345)
...
```

↓

**Decrypted Output**

```
Hello, World!
```

---

## Educational Purpose

This project is intended for:

- Cryptography learning
- Information security coursework
- Understanding public-key encryption
- Demonstrating the ElGamal cryptosystem

---

## Future Improvements

- Graphical User Interface (GUI)
- Support for larger files
- Digital signature implementation
- Random prime number generation
- Improved key management
- Performance optimization

---

## Author

**Iqbal Hafidz Ramadhan**

GitHub: https://github.com/Resync02

---

## License

This project is intended for educational and research purposes. Feel free to use and modify it for learning.
