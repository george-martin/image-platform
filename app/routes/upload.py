import uuid

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.image import Image
from app.services.s3 import upload_file
from app.services.sqs import send_message_to_sqs
from app.constants import ALLOWED_IMAGE_TYPES

router = APIRouter()


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    image_id = str(uuid.uuid4())
    key = f"originals/{image_id}_{file.filename}"

    await upload_file(file.file, key)
    image = Image(
        id=image_id,
        original_key=key,
        status="queued" 
    )

    db.add(image)
    await db.commit()

    await send_message_to_sqs({
        "image_id": image_id,
        "s3_key": key
    })

    return {"image_id": image_id, "status": "queued"}