from passlib.hash import bcrypt

def hash_password(password: str):
    return bcrypt.hash(password)

def verify_password(password, hashed):
    return bcrypt.verify(password, hashed)