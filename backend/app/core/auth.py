from fastapi import Header, HTTPException

from app.core.config import settings


async def require_admin(x_api_key: str = Header(alias="X-API-Key")):
    if x_api_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
