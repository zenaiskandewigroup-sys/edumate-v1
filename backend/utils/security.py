# security.py - password hash & verify
import hashlib
import hmac
import os

def hash_password(password: str) -> str:
    # simple salted sha256 (salt stored with hashed password not used here for simplicity)
    salt = os.getenv("PWD_SALT", "edumate_salt_default")
    return hashlib.sha256((salt + password).encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(password), hashed)


