# Windows Registry Forensics Tool

This tool is designed for analyzing Windows Registry data and helps with forensic investigations. It can extract useful information like the last logged-in user, installed programs, recently accessed files, and more.

## Features
- **Last Logged-In User**: Retrieve details of the last logged-in user.
- **Installed Programs**: List of programs installed on the system.
- **Recently Opened Files**: List of files that have been recently accessed.
- **Running Processes**: Display currently running processes on the system.
- **Registry Monitoring**: Provides the ability to monitor specific registry keys for changes.

## Requirements
- Python 3.x
- `psutil` library (for process and system information)
- `winreg` library (for Windows registry access)

### Install Dependencies
To get started, you'll need to install the necessary dependencies. Run the following command to install them:
```bash
pip install psutil
