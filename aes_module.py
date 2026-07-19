from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16
KEY_PATH = "keys/aes_key.bin"


def pad(data):
    padding = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding]) * padding


def unpad(data):
    padding = data[-1]
    return data[:-padding]


def generate_aes_key():
    key = get_random_bytes(32)

    with open(KEY_PATH, "wb") as f:
        f.write(key)

    return key


def load_aes_key():
    with open(KEY_PATH, "rb") as f:
        return f.read()


def encrypt_file(input_file, output_file, key):
    cipher = AES.new(key, AES.MODE_ECB)

    with open(input_file, "rb") as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(pad(plaintext))

    with open(output_file, "wb") as f:
        f.write(ciphertext)


def decrypt_file(input_file, output_file, key):
    cipher = AES.new(key, AES.MODE_ECB)

    with open(input_file, "rb") as f:
        ciphertext = f.read()

    plaintext = unpad(cipher.decrypt(ciphertext))

    with open(output_file, "wb") as f:
        f.write(plaintext)