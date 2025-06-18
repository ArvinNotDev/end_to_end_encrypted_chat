from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

def encrypt_group_key_with_user_public_key(group_key: bytes, user_public_key_pem: str) -> str:
    """
    Encrypts a symmetric group key using a user's public RSA key.
    Returns base64-encoded encrypted string.
    """
    public_key = serialization.load_pem_public_key(user_public_key_pem.encode())
    encrypted = public_key.encrypt(
        group_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode()
