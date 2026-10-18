from fastapi import APIRouter, UploadFile
import shutil

from src.tasks.tasks import compress_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post('', summary="Загрузить изображение")
async def upload_image(file: UploadFile):
    file_path = f'src/static/images/{file.filename}'
    with open(file_path, 'wb+') as new_file:
        shutil.copyfileobj(file.file, new_file)
    compress_image.delay(file_path)
