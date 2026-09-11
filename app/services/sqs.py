import asyncio
import json
import boto3
from app.config import settings

sqs = boto3.client(
    "sqs",
    region_name=settings.aws_region,
)

def _send_message(payload: dict):
    sqs.send_message(
        QueueUrl=settings.sqs_queue_url,
        MessageBody=json.dumps(payload),
    )

async def send_message_to_sqs(payload: dict):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _send_message, payload)

