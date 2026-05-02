import bcrypt
from core import Settings
from jose import jwt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_access_token(data: dict):
    return jwt.encode(data, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])