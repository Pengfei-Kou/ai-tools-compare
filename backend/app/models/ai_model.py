from datetime import datetime

from sqlalchemy import DateTime, Float, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AIModel(Base):
    __tablename__ = "ai_models"
    __table_args__ = (
        Index("ix_ai_models_provider", "provider"),
        Index("ix_ai_models_category", "category"),
        Index("ix_ai_models_input_price", "input_price"),
        Index("ix_ai_models_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    provider: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    input_price: Mapped[float] = mapped_column(Float, comment="$ per 1M input tokens")
    output_price: Mapped[float] = mapped_column(Float, comment="$ per 1M output tokens")
    context_window: Mapped[int] = mapped_column(Integer, comment="max tokens")

    category: Mapped[str] = mapped_column(String(20), default="chat")
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
