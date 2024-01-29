# utils.py
import secrets

def generate_otp():
    return secrets.randbelow(10000)
