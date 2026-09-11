import aioboto3
from app.config import settings

session = aioboto3.Session()

async def upload_file(file_obj, key: str):
    async with session.client(
        "s3",
        region_name=settings.aws_region,
    ) as s3:
        await s3.upload_fileobj(file_obj, settings.s3_bucket, key)