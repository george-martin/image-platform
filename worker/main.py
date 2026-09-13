import asyncio
import json

import aioboto3
from app.config import settings

session = aioboto3.Session()

async def poll_messages():
    async with session.client(
        "sqs",
        region_name=settings.aws_region,
    ) as sqs:
        while True:
            response = await sqs.receive_message(
                QueueUrl=settings.sqs_queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20,
            )

            messages = response.get("Messages", [])
            if not messages:
                continue
            
            for message in messages:
                print("Received message:", json.loads(message["Body"]))

asyncio.run(poll_messages())