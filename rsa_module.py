import rsa
import os

PUBLIC_KEY_PATH = "keys/public.pem"
PRIVATE_KEY_PATH = "keys/private.pem"

def generate_keys():

    os.makedirs("keys", exist_ok=True)

    public_key, private_key = rsa.newkeys(2048)

    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(public_key.save_pkcs1())

    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(private_key.save_pkcs1())

def load_keys():

    with open(PUBLIC_KEY_PATH, "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(
            f.read()
        )

    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = rsa.PrivateKey.load_pkcs1(
            f.read()
        )

    return public_key, private_key

def sign_hash(hash_value, private_key):

    signature = rsa.sign(
        hash_value.encode(),
        private_key,
        "SHA-256"
    )

    with open(
        "output/signature.sig",
        "wb"
    ) as f:

        f.write(signature)

def verify_signature(hash_value, public_key):

    with open(
        "output/signature.sig",
        "rb"
    ) as f:

        signature = f.read()

    try:

        rsa.verify(
            hash_value.encode(),
            signature,
            public_key
        )

        return True

    except:
        return False