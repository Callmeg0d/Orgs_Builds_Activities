from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.config import settings


def verify_api_key(x_api_key: str = Header(...)):
    """Проверка API ключа"""
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный API ключ"
        )
    return x_api_key


async def get_current_db(db: AsyncSession = Depends(get_db)):
    """Получение сессии базы данных"""
    return db
