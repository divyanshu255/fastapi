from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.database import db
from app.utils.jwt_handler import decode_token
from app.utils.crypto import encrypt_id, decrypt_id
import os
from fastapi.security import HTTPBearer

router = APIRouter()
auth_scheme = HTTPBearer()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload(token=Depends(auth_scheme), file: UploadFile = File(...)):
    user = decode_token(token.credentials)
    if user["role"] != "ops":
        raise HTTPException(403, "Only Ops allowed")
    ext = file.filename.split(".")[-1]
    if ext not in ["docx", "pptx", "xlsx"]:
        raise HTTPException(400, "Invalid file type")
    path = f"{UPLOAD_DIR}/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    result = await db.files.insert_one({"filename": file.filename, "uploader": user["email"]})
    return {"msg": "Uploaded", "id": str(result.inserted_id)}

@router.get("/list")
async def list_files(token=Depends(auth_scheme)):
    user = decode_token(token.credentials)
    if user["role"] != "client":
        raise HTTPException(403, "Clients only")
    files = await db.files.find().to_list(100)
    return files

@router.get("/generate-link/{file_id}")
async def generate_link(file_id: str, token=Depends(auth_scheme)):
    user = decode_token(token.credentials)
    if user["role"] != "client":
        raise HTTPException(403, "Clients only")
    encrypted = encrypt_id(file_id)
    return {"download-link": f"/file/download/{encrypted}"}

@router.get("/download/{enc_id}")
async def download_file(enc_id: str, token=Depends(auth_scheme)):
    user = decode_token(token.credentials)
    if user["role"] != "client":
        raise HTTPException(403, "Only clients can access download")
    try:
        file_id = decrypt_id(enc_id)
    except:
        raise HTTPException(400, "Invalid link")
    file = await db.files.find_one({"_id": file_id})
    if not file:
        raise HTTPException(404, "File not found")
    return {"file": file["filename"]}
