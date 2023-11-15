import os
from encryption_utils import decrypt_file, load_key
import sys
import json

def key_lookup_func(key_id):
    """
    Retrieves the encryption key based on the key identifier.

    Args:
    key_id (str): The key identifier.

    Returns:
    bytes: The encryption key.
    """
    # Assuming the key file is named 'key_<key_id>.key' and stored in a 'keys' directory
    key_file = os.path.join('keys', f'key_{key_id}.key')
    if os.path.exists(key_file):
        return load_key(key_file)
    else:
        raise ValueError(f"No key found for key identifier: {key_id}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt_backup.py <path_to_encrypted_backup>")
        sys.exit(1)

    encrypted_backup_path = sys.argv[1]

    try:
        # Read the key identifier from the encrypted file's metadata
        with open(encrypted_backup_path, 'rb') as file:
            metadata_bytes = file.readline()
        metadata = json.loads(metadata_bytes.decode())
        key_id = metadata['key_id']

        # Decrypt the file using the key_id to retrieve the actual key
        decrypt_file(encrypted_backup_path, lambda key_id=key_id: key_lookup_func(key_id))
        print(f"Decrypted backup file saved at {encrypted_backup_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding metadata: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
