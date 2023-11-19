#!/usr/bin/env python3
import subprocess
import getpass
import is_mysql_active
from dotenv import load_dotenv, set_key
import os
import base64

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

def does_mysql_user_exist(username):
    """
    Checks if a MySQL user exists.

    Args:
    username (str): The username to check for.

    Returns:
    bool: True if the user exists, False otherwise.
    """
    check_user_command = f"SELECT COUNT(*) FROM mysql.user WHERE user = '{username}'"
    try:
        result = subprocess.run(['mysql', '-NBe', check_user_command], capture_output=True, text=True)
        return result.stdout.strip() == "1"
    except subprocess.CalledProcessError as e:
        print(f"Error checking MySQL user: {e}")
        return False

def create_new_user(username):
    print(f"Creating new user '{username}'.")
        password = getpass.getpass("Enter a new password for MySQL: ")
        create_user_command = f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';"
        grant_privileges_command = f"GRANT SELECT, LOCK TABLES ON *.* TO '{username}'@'localhost';"
        try:
            run_mysql_command(create_user_command)
            run_mysql_command(grant_privileges_command)
            print(f"User '{username}' created successfully for MySQL.")
            return password
        except Exception as e:
            print(f"Failed to create user for MySQL: {e}")
            return ""

def setup_mysql_user(env_file, want_new_user):
    """
    Sets up or updates a MySQL user for backup purposes and stores credentials in .env file.

    Args:
    env_file (str): Path to the .env file.
    """
    username = input("Enter the username for MySQL: ")
    
    # Log into existing user
    if does_mysql_user_exist(username) && want_new_user == False:
        print(f"User '{username}' found.")
        password = getpass.getpass("Enter the existing password for this MySQL user: ")
    # Trying to create a new user with existing username 
    elif does_mysql_user_exist(username) && want_new_user:
        print(f"User '{username}' exists.")
        login = input(f"Do you want to log into '{username}'? (y/n): ").lower()
        if login == 'y':
            password = getpass.getpass("Enter the existing password for this MySQL user: ")
        elif login == 'n':
            username = input("Enter the username for a new MySQL user: ")
            password = create_new_user(username)
            if password == "":
                return
        else:
            print("Invalid input.")
            return
    # Trying to use a user that does not exist    
    elif !does_mysql_user_exist(username) && want_new_user == False:
        print("User does not exist.")
        login = input("Do you want to log into an existing user? (y/n): ").lower()
        if login == 'y':
            username = input("Enter the username for MySQL: ")
            password = getpass.getpass("Enter the existing password for this MySQL user: ")
        elif login == 'n':
    # Creating a new MySQL user    
    else:
        _______________________________________________________________________________________
        print(f"Creating new user '{username}'.")
        password = getpass.getpass("Enter a new password for MySQL: ")
        create_user_command = f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';"
        grant_privileges_command = f"GRANT SELECT, LOCK TABLES ON *.* TO '{username}'@'localhost';"
        try:
            run_mysql_command(create_user_command)
            run_mysql_command(grant_privileges_command)
            print(f"User '{username}' created successfully for MySQL.")
        except Exception as e:
            print(f"Failed to create user for MySQL: {e}")
            return
            __________________________________________________________________________

    # Save credentials in .env file
    set_key(env_file, "MYSQL_USER", username)
    set_key(env_file, "MYSQL_PASSWORD", password)
    print(f"Credentials for '{username}' are saved in '{env_file}'.")


def setup_global_passphrase_and_salt(env_file):
    """
    Sets up a global passphrase for encryption and a random salt, and stores them in the .env file.

    Args:
    env_file (str): Path to the .env file.
    """
    passphrase = getpass.getpass("Enter a global passphrase for encryption: ")
    set_key(env_file, "GLOBAL_PASSPHRASE", passphrase)

    salt = os.urandom(16)
    set_key(env_file, "ENCRYPTION_SALT", base64.b64encode(salt).decode())
    print("Global passphrase and salt have been set.")

def main():
    env_file = '.env'
    ensure_env_file_exists(env_file)
    load_dotenv(env_file)

    # Check if global passphrase and salt are already set
    if not os.getenv("GLOBAL_PASSPHRASE") or not os.getenv("ENCRYPTION_SALT"):
        setup_global_passphrase_and_salt(env_file)

    # Check for MySQL service
        if is_mysql_active.is_mysql_service_active():
            print("MySQL service is active.")
            user_input = input("Do you want to create a new MySQL user for backups? (y/n): ").lower()
            if user_input == 'y':
                setup_mysql_user(env_file, want_new_user: bool = True)
            elif user_input == 'n':
                setup_mysql_user(env_file, want_new_user: bool = False)
            else:
                print("Invalid input. Exiting setup.")
        else:
            print("MySQL service is not active or not present.")

if __name__ == "__main__":
    main()
