from PIL import Image
import os
from src.tasks.celery_app import celery_instance


@celery_instance.task(name="compress_image")
def compress_image(image_path: str, quality: int = 85):
    output_dir = 'src/static/images/compressed'
    sizes = [1024, 512, 256]

    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(image_path)

    # JPEG не поддерживает прозрачность — конвертируем
    if img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    saved_files = []

    for size in sizes:
        ratio = size / max(img.size)

        # Не увеличиваем маленькие изображения
        if ratio >= 1:
            resized = img.copy()
        else:
            new_size = (round(img.width * ratio), round(img.height * ratio))
            resized = img.resize(new_size, Image.LANCZOS)

        output_path = os.path.join(output_dir, f"{base_name}_{size}.jpg")
        resized.save(output_path, quality=quality, optimize=True)
        saved_files.append(output_path)

    return saved_files
