import asyncio
import boto3
from app.config import settings

s3 = boto3.client(
    "s3",
    region_name=settings.aws_region,
)
def _upload_file(file_obj, key: str):
    s3.upload_fileobj(file_obj, settings.s3_bucket, key)

async def upload_file(file_obj, key: str):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _upload_file, file_obj, key)
    return f"s3://{settings.s3_bucket}/{key}"