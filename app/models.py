from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str
    role: str  

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FileInfo(BaseModel):
    filename: str
    uploader: str
