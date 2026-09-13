import aioboto3
from app.config import settings

session = aioboto3.Session()

async def upload_file(file_obj, key: str):
    async with session.client(
        "s3",
        region_name=settings.aws_region,
    ) as s3:
        await s3.upload_fileobj(file_obj, settings.s3_bucket, key)

async def download_file(key: str) -> bytes:
    async with session.client(
        "s3",
        region_name=settings.aws_region,
    ) as s3:
        response = await s3.get_object(Bucket=settings.s3_bucket, Key=key)
        return await response["Body"].read()

async def upload_bytes(data: bytes, key: str, content_type: str):
    async with session.client(
        "s3",
        region_name=settings.aws_region,
    ) as s3:
        await s3.put_object(
            Bucket=settings.s3_bucket,
            Key=key,
            Body=data,
            ContentType=content_type,
        )