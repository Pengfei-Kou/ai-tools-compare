from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.ai_model import AIModel
from app.schemas.ai_model import AIModelCreate, AIModelList, AIModelResponse

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/", response_model=AIModelList)
async def list_models(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AIModel).where(AIModel.is_active.is_(True)))
    models = result.scalars().all()
    return AIModelList(models=models, total=len(models))


@router.get("/{model_id}", response_model=AIModelResponse)
async def get_model(model_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AIModel).where(AIModel.id == model_id))
    model = result.scalar_one()
    return model


@router.post("/", response_model=AIModelResponse, status_code=201)
async def create_model(data: AIModelCreate, db: AsyncSession = Depends(get_db)):
    model = AIModel(**data.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model
