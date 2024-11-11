import winreg
import os
import psutil
from datetime import datetime

# Function to access registry keys and values
def get_registry_value(hive, subkey, value_name):
    try:
        key = winreg.OpenKey(hive, subkey)
        value, regtype = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return value
    except FileNotFoundError:
        return None

# Function to get the last logged in user
def get_last_logged_in_user():
    user = get_registry_value(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI", "LastLoggedOnUser")
    if user:
        return user
    else:
        return "Not Available"

# Function to get the list of installed programs
def get_installed_programs():
    installed_programs = []
    program_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    for key in program_keys:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key)
            for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                subkey_name = winreg.EnumKey(reg_key, i)
                try:
                    subkey = winreg.OpenKey(reg_key, subkey_name)
                    display_name = get_registry_value(winreg.HKEY_LOCAL_MACHINE, os.path.join(key, subkey_name), "DisplayName")
                    if display_name:
                        installed_programs.append(display_name)
                except Exception as e:
                    pass
            winreg.CloseKey(reg_key)
        except FileNotFoundError:
            pass
    return installed_programs

# Function to get recent file activity (user recently opened files)
def get_recent_files():
    recent_files = []
    recent_file_path = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Recent")
    if os.path.exists(recent_file_path):
        for file in os.listdir(recent_file_path):
            file_path = os.path.join(recent_file_path, file)
            recent_files.append(file_path)
    return recent_files

# Function to get the process running on the system
def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        processes.append(proc.info)
    return processes

# Function to log information to a file
def log_info(log_file, message):
    with open(log_file, 'a') as f:
        f.write(message + "\n")

# Main function to run the tool and gather forensic data
def run_registry_forensics():
    log_file = "registry_forensics_log.txt"

    # Log Last Logged in User
    last_logged_in_user = get_last_logged_in_user()
    log_info(log_file, f"Last Logged in User: {last_logged_in_user}")

    # Log Installed Programs
    installed_programs = get_installed_programs()
    log_info(log_file, f"Installed Programs: {', '.join(installed_programs)}")

    # Log Recent Files Opened
    recent_files = get_recent_files()
    log_info(log_file, f"Recent Files Opened: {', '.join(recent_files)}")

    # Log Running Processes
    running_processes = get_running_processes()
    log_info(log_file, "Running Processes:")
    for proc in running_processes:
        log_info(log_file, f"PID: {proc['pid']}, Name: {proc['name']}, User: {proc['username']}")

    # Display and log complete information
    print(f"Last Logged in User: {last_logged_in_user}")
    print(f"Installed Programs: {', '.join(installed_programs)}")
    print(f"Recent Files Opened: {', '.join(recent_files)}")
    print("Running Processes:")
    for proc in running_processes:
        print(f"PID: {proc['pid']}, Name: {proc['name']}, User: {proc['username']}")
    
    print(f"All forensic data has been logged to {log_file}")

# Run the tool
if __name__ == "__main__":
    run_registry_forensics()
