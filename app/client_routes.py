


from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from app.utils.jwt_handler import decode_token
from app.utils.crypto import encrypt_id, decrypt_id
from app.database import db

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get("/files", tags=["Client"])
async def list_all_files(token=Depends(auth_scheme)):
    user = decode_token(token.credentials)
    if user["role"] != "client":
        raise HTTPException(status_code=403, detail="Only client users can view files")
    files = await db.files.find().to_list(100)
    return {"files": files}


@router.get("/generate-download-link/{file_id}", tags=["Client"])
async def generate_download_link(file_id: str, token=Depends(auth_scheme)):
    user = decode_token(token.credentials)
    if user["role"] != "client":
        raise HTTPException(status_code=403, detail="Only client users can generate download links")

    enc_id = encrypt_id(file_id)
    return {
        "download-link": f"/client/download/{enc_id}",
        "message": "success"
    }


@router.get("/download/{enc_id}", tags=["Client"])
async def download_file(enc_id: str, token=Depends(auth_scheme)):
    user = decode_token(token.credentials)
    if user["role"] != "client":
        raise HTTPException(status_code=403, detail="Only client users can download files")

    try:
        file_id = decrypt_id(enc_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid or expired link")

    file_record = await db.files.find_one({"_id": file_id})
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    return {"filename": file_record["filename"]}
