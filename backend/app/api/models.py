import math
from enum import Enum

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import require_admin
from app.core.database import get_db
from app.models.ai_model import AIModel
from app.schemas.ai_model import AIModelCreate, AIModelList, AIModelResponse

router = APIRouter(prefix="/models", tags=["models"])


class SortField(str, Enum):
    name = "name"
    provider = "provider"
    input_price = "input_price"
    output_price = "output_price"
    context_window = "context_window"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("/", response_model=AIModelList)
async def list_models(
    db: AsyncSession = Depends(get_db),
    provider: str | None = Query(None, description="Filter by provider name"),
    category: str | None = Query(None, description="Filter by category"),
    sort_by: SortField = Query(SortField.input_price, description="Sort field"),
    order: SortOrder = Query(SortOrder.asc, description="Sort direction"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
):
    query = select(AIModel).where(AIModel.is_active.is_(True))

    if provider:
        query = query.where(AIModel.provider == provider)
    if category:
        query = query.where(AIModel.category == category)

    sort_column = getattr(AIModel, sort_by.value)
    if order == SortOrder.desc:
        sort_column = sort_column.desc()
    query = query.order_by(sort_column)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    models = result.scalars().all()

    return AIModelList(
        models=models,
        total=total,
        page=page,
        per_page=per_page,
        pages=math.ceil(total / per_page),
    )


@router.get("/{model_id}", response_model=AIModelResponse)
async def get_model(model_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AIModel).where(AIModel.id == model_id))
    model = result.scalar_one()
    return model


@router.post("/", response_model=AIModelResponse, status_code=201, dependencies=[Depends(require_admin)])
async def create_model(data: AIModelCreate, db: AsyncSession = Depends(get_db)):
    model = AIModel(**data.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model
