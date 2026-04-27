from pydantic import BaseModel, Field


class AIModelBase(BaseModel):
    name: str
    provider: str
    description: str | None = None
    input_price: float
    output_price: float
    context_window: int
    category: str = "chat"


class AIModelCreate(AIModelBase):
    pass


class AIModelResponse(AIModelBase):
    id: int
    is_active: bool

    model_config = {"from_attributes": True}


class AIModelList(BaseModel):
    models: list[AIModelResponse]
    total: int
    page: int = Field(description="Current page number")
    per_page: int = Field(description="Items per page")
    pages: int = Field(description="Total number of pages")
