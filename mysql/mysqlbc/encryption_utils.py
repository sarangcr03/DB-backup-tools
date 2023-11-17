from cryptography.fernet import Fernet
import json
import os
from dotenv import load_dotenv
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

load_dotenv()
GLOBAL_PASSPHRASE = os.getenv("GLOBAL_PASSPHRASE")
ENCRYPTION_SALT = base64.b64decode(os.getenv("ENCRYPTION_SALT"))
SALT = base64.b64decode(os.getenv("ENCRYPTION_SALT"))

def passphrase_to_key(passphrase):
    """
    Derives a Fernet key from a passphrase.

    Args:
    passphrase (str): The passphrase used for key derivation.

    Returns:
    bytes: A key derived from the passphrase.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

def generate_key():
    """
    Generates a new encryption key.
    """
    return Fernet.generate_key()

def save_key(key, key_file, passphrase):
    fernet = Fernet(passphrase_to_key(passphrase))
    encrypted_key = fernet.encrypt(key)
    with open(key_file, 'wb') as file:
        file.write(encrypted_key)

def load_key(key_file, passphrase):
    fernet = Fernet(passphrase_to_key(passphrase))
    with open(key_file, 'rb') as file:
        encrypted_key = file.read()
    return fernet.decrypt(encrypted_key)

def encrypt_file(file_path, key, key_identifier):
    fernet = Fernet(key)

    # Read the original file content
    with open(file_path, 'rb') as file:
        original_data = file.read()

    # Encrypt the original data
    encrypted_data = fernet.encrypt(original_data)

    # Prepare and encode the metadata
    metadata = json.dumps({'key_id': key_identifier})
    metadata_bytes = metadata.encode()

    # Write the metadata and encrypted data to the file
    with open(file_path, 'wb') as file:
        file.write(metadata_bytes + b'\n' + encrypted_data)

def decrypt_file(file_path, key_lookup_func):
    with open(file_path, 'rb') as file:
        metadata_bytes, encrypted_data = file.read().split(b'\n', 1)

    metadata = json.loads(metadata_bytes.decode())
    key_id = metadata['key_id']

    actual_key = key_lookup_func(key_id)
    if not actual_key:
        raise ValueError("Key not found for identifier:", key_id)

    fernet = Fernet(actual_key)
    decrypted_file_data = fernet.decrypt(encrypted_data)

    with open(file_path, 'wb') as file:
        file.write(decrypted_file_data)



