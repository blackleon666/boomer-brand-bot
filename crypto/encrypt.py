from cryptography.fernet import Fernet
import os

# In a real application, the key should be loaded from an environment variable or a secure vault.
# For this project, we expect the key to be set in the ENCRYPTION_KEY environment variable.
def get_cipher():
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY environment variable is not set")
    return Fernet(key.encode())

def encrypt_text(plaintext: str) -> str:
    """Encrypt a plaintext string and return the encrypted string."""
    cipher = get_cipher()
    encrypted_bytes = cipher.encrypt(plaintext.encode())
    return encrypted_bytes.decode()

def decrypt_text(encrypted_text: str) -> str:
    """Decrypt an encrypted string and return the plaintext."""
    cipher = get_cipher()
    decrypted_bytes = cipher.decrypt(encrypted_text.encode())
    return decrypted_bytes.decode()
