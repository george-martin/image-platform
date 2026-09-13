from app.db import AsyncSessionLocal

# docker compose exec postgres psql -U postgres -d image_platform
async def update_image_status(image_id: str, status: str):
    async with AsyncSessionLocal() as db:
        from app.models.image import Image

        image = await db.get(Image, image_id)

        if image:
            image.status = status
            await db.commit()