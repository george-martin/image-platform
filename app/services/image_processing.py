from io import BytesIO

from PIL import Image


def resize_image(image_data: bytes, max_size: int = 1000) -> bytes:
    image = Image.open(BytesIO(image_data))

    image.thumbnail((max_size, max_size))

    image = image.convert("RGB")

    output = BytesIO()

    image.save(
        output,
        format="JPEG",
        quality=85,
    )

    return output.getvalue()