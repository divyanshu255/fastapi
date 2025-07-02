
# app/ops_routes.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import HTTPBearer
from app.utils.jwt_handler import decode_token
from app.database import db
import os

router = APIRouter()
auth_scheme = HTTPBearer()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", tags=["Ops"])
async def upload_file(token=Depends(auth_scheme), file: UploadFile = File(...)):
    user = decode_token(token.credentials)
    if user["role"] != "ops":
        raise HTTPException(status_code=403, detail="Only ops users can upload files")

    filename = file.filename
    ext = filename.split(".")[-1]
    if ext not in ["docx", "pptx", "xlsx"]:
        raise HTTPException(status_code=400, detail="Only .docx, .pptx, .xlsx files allowed")

    save_path = os.path.join(UPLOAD_DIR, filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())

    result = await db.files.insert_one({
        "filename": filename,
        "uploader": user["email"]
    })

    return {"message": "File uploaded", "id": str(result.inserted_id)}
