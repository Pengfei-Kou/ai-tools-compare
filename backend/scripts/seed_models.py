"""Seed initial AI model data into the database."""
import asyncio

from sqlalchemy import select

from app.core.database import async_session
from app.models.ai_model import AIModel

MODELS_DATA = [
    # OpenAI
    {"name": "GPT-5.4", "provider": "OpenAI", "description": "OpenAI's latest flagship model", "input_price": 2.50, "output_price": 15.00, "context_window": 400000, "category": "chat"},
    {"name": "GPT-5.4 Mini", "provider": "OpenAI", "description": "Cost-effective version of GPT-5.4", "input_price": 0.75, "output_price": 4.50, "context_window": 400000, "category": "chat"},
    {"name": "GPT-5.4 Nano", "provider": "OpenAI", "description": "Smallest GPT-5.4 variant for high-volume tasks", "input_price": 0.20, "output_price": 1.25, "context_window": 200000, "category": "chat"},
    {"name": "GPT-5", "provider": "OpenAI", "description": "Standard GPT-5 model", "input_price": 1.25, "output_price": 10.00, "context_window": 400000, "category": "chat"},
    {"name": "GPT-5 Mini", "provider": "OpenAI", "description": "Lightweight GPT-5 for everyday tasks", "input_price": 0.25, "output_price": 2.00, "context_window": 400000, "category": "chat"},
    {"name": "GPT-5 Nano", "provider": "OpenAI", "description": "Cheapest GPT-5 variant", "input_price": 0.05, "output_price": 0.40, "context_window": 200000, "category": "chat"},
    {"name": "GPT-5 Pro", "provider": "OpenAI", "description": "Premium tier with enhanced capabilities", "input_price": 15.00, "output_price": 120.00, "context_window": 400000, "category": "chat"},

    # Anthropic
    {"name": "Claude Opus 4.6", "provider": "Anthropic", "description": "Anthropic's most powerful reasoning model", "input_price": 5.00, "output_price": 25.00, "context_window": 500000, "category": "chat"},
    {"name": "Claude Sonnet 4.6", "provider": "Anthropic", "description": "Balanced quality and cost", "input_price": 3.00, "output_price": 15.00, "context_window": 500000, "category": "chat"},

    # Google
    {"name": "Gemini 3.1 Pro", "provider": "Google", "description": "Google's flagship reasoning model with 2M context", "input_price": 2.00, "output_price": 12.00, "context_window": 2000000, "category": "chat"},
    {"name": "Gemini 3.0 Flash", "provider": "Google", "description": "Fast and cost-effective frontier model", "input_price": 0.50, "output_price": 3.00, "context_window": 1000000, "category": "chat"},

    # DeepSeek
    {"name": "DeepSeek V4", "provider": "DeepSeek", "description": "Latest DeepSeek model with improved coding", "input_price": 0.30, "output_price": 0.50, "context_window": 1000000, "category": "chat"},
    {"name": "DeepSeek R1", "provider": "DeepSeek", "description": "Reasoning-focused model", "input_price": 0.55, "output_price": 2.19, "context_window": 128000, "category": "reasoning"},
    {"name": "DeepSeek Chat V3.2", "provider": "DeepSeek", "description": "Previous generation chat model", "input_price": 0.28, "output_price": 0.42, "context_window": 128000, "category": "chat"},
]


async def seed():
    async with async_session() as session:
        existing = await session.execute(select(AIModel.name))
        existing_names = {row[0] for row in existing.all()}

        added = 0
        skipped = 0
        for data in MODELS_DATA:
            if data["name"] in existing_names:
                print(f"  skip (exists): {data['name']}")
                skipped += 1
                continue
            session.add(AIModel(**data))
            print(f"  add: {data['name']}")
            added += 1

        await session.commit()
        print(f"\nDone. Added {added}, skipped {skipped} existing.")


if __name__ == "__main__":
    asyncio.run(seed())
