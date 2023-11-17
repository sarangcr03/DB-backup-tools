#!/usr/bin/env python3
import argparse
import subprocess
import os
import uuid
from dotenv import load_dotenv
from encryption_utils import encrypt_file, decrypt_file, generate_key, save_key

load_dotenv()
GLOBAL_PASSPHRASE = os.getenv("GLOBAL_PASSPHRASE")


def backup_mysql_database(backup_path, db_name="all"):
    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")

    try:
        # Form the mysqldump command
        if db_name == "all":
            command = f"mysqldump --all-databases --user={mysql_user} --password={mysql_password}"
        else:
            command = f"mysqldump --user={mysql_user} --password={mysql_password} {db_name}"
        
        # Execute the command and save the output to a file
        with open(backup_path, 'w') as file:
            subprocess.run(command.split(), stdout=file, check=True)

        # Generate a unique key identifier for the backup
        key_id = str(uuid.uuid4())

        # Generate and save a new encryption key associated with this key_id
        new_key = generate_key()
        save_key(new_key, f'key_{key_id}.key', GLOBAL_PASSPHRASE)

        # Encrypt the backup file using the new key
        encrypt_file(backup_path, new_key, key_id)
        
        print(f"Encrypted backup of '{db_name}' database saved to '{backup_path}' using key ID: {key_id}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
         
def parse_arguments():
    parser = argparse.ArgumentParser(description="MySQL Database Backup Tool")
    parser.add_argument("-d", "--database", help="Name of the database to backup. Default: all databases.", default="all")
    parser.add_argument("-o", "--output", help="Output path for the backup file")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Perform backup based on the provided arguments
    if args.output:
        backup_mysql_database(args.output, args.database)

if __name__ == "__main__":
    main()
