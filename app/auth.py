from fastapi import APIRouter, HTTPException
from app.models import User, UserLogin
from app.utils.jwt_handler import create_token
from app.utils.email_sender import send_verification_email
from passlib.context import CryptContext
from app.database import db

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup")
async def signup(user: User):
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(400, "Email exists")
    hashed = pwd_context.hash(user.password)
    await db.users.insert_one({**user.dict(), "password": hashed, "verified": False})
    token = create_token({"email": user.email, "type": "verify"})
    send_verification_email(user.email, token)
    return {"msg": "Check your email to verify"}

@router.get("/verify-email")
async def verify_email(token: str):
    from app.utils.jwt_handler import decode_token
    data = decode_token(token)
    await db.users.update_one({"email": data["email"]}, {"$set": {"verified": True}})
    return {"msg": "Email verified"}

@router.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(401, "Invalid credentials")
    if not db_user.get("verified"):
        raise HTTPException(403, "Email not verified")
    token = create_token({"email": db_user["email"], "role": db_user["role"]})
    return {"token": token}
