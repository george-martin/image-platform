import aioboto3
import json
from app.config import settings

session = aioboto3.Session()

async def send_message_to_sqs(message: dict):
    async with session.client(
        "sqs",
        region_name=settings.aws_region,
    ) as sqs:
        response = await sqs.send_message(
            QueueUrl=settings.sqs_queue_url,
            MessageBody=json.dumps(message),
        )

        return response

async def delete_message(receipt_handle: str):
    async with session.client(
        "sqs",
        region_name=settings.aws_region,
    ) as sqs:
        await sqs.delete_message(
            QueueUrl=settings.sqs_queue_url,
            ReceiptHandle=receipt_handle,
        )