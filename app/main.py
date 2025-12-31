from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .database import init_db
from .auth import create_access_token, get_current_user, verify_password, get_password_hash
from .routers import post
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    await init_db()
    yield

app = FastAPI(
    title="FastAPI Async Blog API",
    description="Uma API de blog moderna e assíncrona com PostgreSQL, JWT e Frontend Integrado.",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Paulo Carlos Filho",
        "url": "https://github.com/paulocarlosfilho",
    },
    license_info={
        "name": "MIT",
    },
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Error Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro interno no servidor. Por favor, tente novamente mais tarde."},
    )

# Mock de usuário (Em um sistema real, isso viria do banco de dados)
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("admin123"),
    }
}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = FAKE_USERS_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}

app.include_router(post.router)

# Mount Static Files
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
