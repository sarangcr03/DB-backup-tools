#!/usr/bin/env python3
import subprocess

def is_mysql_service_active():
    """
    Checks if the MySQL service is active on the system.

    Returns:
    bool: True if the MySQL service is active, False otherwise.
    """
    try:
        result = subprocess.run(['systemctl', 'is-active', 'mysql'], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True, 
                                check=True)
        
        return result.stdout.strip() == 'active'
    except subprocess.CalledProcessError as e:
        print(f"MySQL service not found or inactive: {e}")
    except FileNotFoundError:
        print("Error: 'systemctl' command not found. Ensure you are running this on a compatible system.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    is_active = is_mysql_service_active()
    print(f"MySQL service active: {is_active}")

