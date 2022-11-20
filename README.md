# Setup
Create virtual environment
    python -m venv env

Activate env then restore packages from requirements.txt 
    pip install -r requirements.txt

# To Run
Run dir_checker.py

# Test SMTP Server
Run your own local python SMTP server from cmd prompt
    python -m smtpd -c DebuggingServer -n 120.0.0.1:1025
