#!/usr/bin/env python3
import subprocess
import getpass
import is_mysql_active
from dotenv import load_dotenv, set_key
import os

def ensure_env_file_exists(env_file_path):
    """
    Checks if the .env file exists at the given path. If not, creates an empty .env file.

    Args:
    env_file_path (str): Path to the .env file.
    """
    if not os.path.exists(env_file_path):
        open(env_file_path, 'a').close()
        print(f"Created a new .env file at: {env_file_path}")

def run_mysql_command(command):
    """
    Executes the given MySQL command.

    Args:
    command (str): MySQL command to execute.
    """
    try:
        subprocess.run(['mysql', '-e', command], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing MySQL command: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def setup_mysql_user(env_file):
    """
    Sets up a new MySQL user with limited privileges for backup purposes and stores credentials in .env file.

    Args:
    env_file (str): Path to the .env file.
    """
    username = input("Enter a new username for MySQL: ")
    password = getpass.getpass("Enter a new password for MySQL: ")

    try:
        # Create MySQL user
        command = f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';"
        run_mysql_command(command)
        # Grant SELECT and LOCK TABLES privileges
        command = f"GRANT SELECT, LOCK TABLES ON *.* TO '{username}'@'localhost';"
        run_mysql_command(command)
        print(f"User {username} created successfully for MySQL.")
        set_key(env_file, "MYSQL_USER", username)
        set_key(env_file, "MYSQL_PASSWORD", password)
        print(f"Credentials for '{username}' are saved in '{env_file}'.")

    except Exception as e:
        print(f"Failed to create user for MySQL: {e}")

def main():
    env_file = '.env'
    ensure_env_file_exists(env_file)
    load_dotenv(env_file)
    # Check for MySQL service
    if is_mysql_active.is_mysql_service_active():
        print("MySQL service is active.")
        if input("Do you want to create a new MySQL user for backups? (y/n): ").lower() == 'y':
            setup_mysql_user(env_file)
    else:
        print("MySQL service is not active or not present.")

if __name__ == "__main__":
    main()
