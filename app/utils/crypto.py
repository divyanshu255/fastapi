
from cryptography.fernet import Fernet
from app.config import FERNET_KEY

fernet = Fernet(FERNET_KEY)

def encrypt_id(id: str) -> str:
    return fernet.encrypt(id.encode()).decode()

def decrypt_id(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
