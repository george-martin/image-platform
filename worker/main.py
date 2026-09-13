import asyncio
import json

import aioboto3
from app.config import settings
from app.services.s3 import download_file, upload_bytes
from app.services.image_processing import resize_image
from worker.db import update_image_status

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
                job = json.loads(message["Body"])
                await update_image_status(job["image_id"], "processing")
                image_data = await download_file(job["s3_key"])
                processed_data = resize_image(image_data)
                processed_key = f"processed/{job['image_id']}.jpg"

                await upload_bytes(
                    processed_data, 
                    processed_key, 
                    content_type="image/jpeg"
                )

                print(f"Uploaded processed image: {processed_key}")

asyncio.run(poll_messages())