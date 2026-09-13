import aioboto3
from app.config import settings

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db

router = APIRouter()
session = aioboto3.Session()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))

    async with session.client(
        "s3",
        region_name=settings.aws_region,
    ) as s3:
        await s3.head_bucket(Bucket=settings.s3_bucket)
    
    async with session.client(
        "sqs",
        region_name=settings.aws_region,
    ) as sqs:
        await sqs.get_queue_attributes(
            QueueUrl=settings.sqs_queue_url,
            AttributeNames=["QueueArn"],
        )

    return {
        "status": "ok",
        "database": "ok",
        "s3": "ok",
        "sqs": "ok",
    }