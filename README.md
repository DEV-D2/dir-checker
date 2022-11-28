Once configured, this program will scan a directory for files and report back to the specified email address. 

Personal use case: 
A downloader software downloads and stores PDF's in a folder on a server. I needed a way to automate checking this folder daily. 

# To Run
1. Run dir_checker.py - this will create an empty config file - "config.cfg".
2. Update "config.cfg" with the required settings. 
3. Run dir_checker.py  - double check the cfg file if you're concerned about the password being stored.

## Password Safety
Because password safety is a thing, on first run through, dir-checker will read the config and null the password field to ensure that the password is no longer stored as plain text. The password is stored in the system's keyring. 

# Dev Env Setup
Create virtual environment
    python -m venv env

Activate env then restore packages from requirements.txt 
    pip install -r requirements.txt

## Testing
You can test locally by creating a dummy STMP server on your machine. 

## Test SMTP Server
Run your own local python SMTP server from cmd prompt
    python -m smtpd -c DebuggingServer -n 120.0.0.1:1025
