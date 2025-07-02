
from passlib.context import CryptContext
from jose import jwt
from app.config import JWT_SECRET, FERNET_KEY
from cryptography.fernet import Fernet

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(FERNET_KEY)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    return jwt.encode(data, JWT_SECRET, algorithm="HS256")

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

def encrypt_id(file_id: str) -> str:
    return fernet.encrypt(file_id.encode()).decode()

def decrypt_id(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
