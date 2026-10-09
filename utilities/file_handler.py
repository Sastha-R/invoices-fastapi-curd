
from pathlib import Path
from uuid import uuid4
import aiofiles

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


async def save_delivery_proof(photo):
    extension = Path(photo.filename).suffix.lower()

    if extension not in [".jpg", ".jpeg", ".png"]:
        raise ValueError("Only JPG and PNG photos are allowed")

    file_name = f"{uuid4().hex}{extension}"
    file_path = UPLOAD_FOLDER / file_name

    content = await photo.read()

    async with aiofiles.open(file_path, "wb") as file:
        await file.write(content)

    return file_name, str(file_path)
