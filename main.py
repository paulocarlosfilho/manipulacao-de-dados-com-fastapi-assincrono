import sqlalchemy as sa
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database import engine, metadata, init_db
from auth import create_access_token, get_current_user, verify_password, get_password_hash
from datetime import timedelta
# Note: I'm keeping the original import structure as much as possible
# but since controllers/post.py doesn't exist, I'll assume it's post.py in the root
try:
    from controllers import post
except ImportError:
    import post

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Close database connections
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
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

if hasattr(post, "router"):
    # Exemplo de como proteger todas as rotas de um router (opcional)
    # app.include_router(post.router, dependencies=[Depends(get_current_user)])
    app.include_router(post.router)

