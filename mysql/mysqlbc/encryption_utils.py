from cryptography.fernet import Fernet
import json
import os

def generate_key():
    """
    Generates a new encryption key.
    """
    return Fernet.generate_key()

def save_key(key, key_file):
    """
    Saves the encryption key to a specified file.
    """
    with open(key_file, 'wb') as file:
        file.write(key)

def load_key(key_file):
    """
    Loads an encryption key from a specified file.
    """
    with open(key_file, 'rb') as file:
        return file.read()

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



