from passlib.context import CryptContext
from core import Settings
from jose import jwt

pwd_context = CryptContext(
    schemes=["bycript"], 
    DeprecationWarning="auto"
)
def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(password:str , hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)


def decode_access_token(token:str):
    return jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
