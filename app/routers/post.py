from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.exc import IntegrityError
from ..database import engine
from ..models.post import post_table
from ..models.post_schema import Post, PostCreate
from ..auth import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(payload: PostCreate):
    try:
        async with engine.begin() as conn:
            query = post_table.insert().values(**payload.model_dump()).returning(post_table)
            result = await conn.execute(query)
            return result.fetchone()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um post com este título."
        )

@router.get("/", response_model=List[Post])
async def read_posts():
    async with engine.connect() as conn:
        query = post_table.select()
        result = await conn.execute(query)
        return result.fetchall()

@router.get("/{post_id}", response_model=Post)
async def read_post(post_id: int):
    async with engine.connect() as conn:
        query = post_table.select().where(post_table.c.id == post_id)
        result = await conn.execute(query)
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Post não encontrado")
        return row

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, payload: PostCreate):
    try:
        async with engine.begin() as conn:
            query = post_table.update().where(post_table.c.id == post_id).values(**payload.model_dump()).returning(post_table)
            result = await conn.execute(query)
            row = result.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Post não encontrado")
            return row
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um post com este título."
        )

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    async with engine.begin() as conn:
        query = post_table.delete().where(post_table.c.id == post_id)
        result = await conn.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Post não encontrado")
        return None
