from fastapi import FastAPI
from app.auth import router as auth_router
from app.client_routes import router as client_router
from app.ops_routes import router as ops_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(client_router, prefix="/client")
app.include_router(ops_router, prefix="/ops")
