import json
import os
from PIL import Image
import numpy as np
from pycocotools import mask as maskUtils
import cv2

# Папка с изображениями и аннотациями YOLOv8
images_folder = './merg/images/train'  # Замените на путь к папке с изображениями
annotations_folder = './merg/labels/train'  # Замените на путь к папке с YOLOv8 аннотациями
output_json = 'output_coco.json'  # Имя выходного файла

# Инициализация COCO аннотаций
coco = {
    "images": [],
    "annotations": [],
    "categories": [],
}

# Список классов (заполните в соответствии с вашими данными)
class_names = ['box', 'container', 'person', 'shelf']  # Замените на реальные имена классов

# Добавляем категории в COCO
for i, class_name in enumerate(class_names):
    coco['categories'].append({
        "id": i+1,
        "name": class_name,
        "supercategory": "none",
    })

annotation_id = 0

# Обработка изображений и аннотаций
for image_id, image_name in enumerate(os.listdir(images_folder)):
    if not image_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    # Открываем изображение для получения размеров
    image_path = os.path.join(images_folder, image_name)
    image = Image.open(image_path)
    width, height = image.size

    # Добавляем изображение в COCO
    coco['images'].append({
        "id": image_id,
        "file_name": image_name,
        "width": width,
        "height": height,
    })

    # Открываем соответствующий файл аннотации
    annotation_path = os.path.join(annotations_folder, image_name.replace('.jpg', '.txt').replace('.png', '.txt'))
    if not os.path.exists(annotation_path):
        continue

    with open(annotation_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        data = list(map(float, line.split()))
        class_id = int(data[0])
        segmentation = data[1:]

        # Проверка на корректное количество координат
        if len(segmentation) < 6 or len(segmentation) % 2 != 0:
            print(f"Неверное количество координат в файле: {annotation_path}")
            continue

        # Преобразуем координаты полигонов в формат для OpenCV
        x_coords = segmentation[0::2]
        y_coords = segmentation[1::2]

        # Масштабирование координат в случае, если они нормализованы (от 0 до 1)
        x_coords = np.array(x_coords) * width
        y_coords = np.array(y_coords) * height

        # Округление координат до целых значений пикселей
        x_coords = np.clip(np.round(x_coords), 0, width - 1)
        y_coords = np.clip(np.round(y_coords), 0, height - 1)

        # Создаем пустую маску изображения
        mask = np.zeros((height, width), dtype=np.uint8)

        # Координаты полигонов как список точек
        polygon = np.array([list(zip(x_coords, y_coords))], dtype=np.int32)

        # Заполнение маски по полигону
        cv2.fillPoly(mask, polygon, 1)

        # Проверка корректности заполнения маски
        if mask.sum() == 0:
            print(f"Предупреждение: Пустая маска для файла {annotation_path}")

        # Преобразуем маску в RLE формат
        rle = maskUtils.encode(np.asfortranarray(mask))

        # Преобразуем RLE в сериализуемый формат
        rle['counts'] = rle['counts'].decode('utf-8')  # Конвертация bytes в строку

        # Вычисляем bounding box из RLE
        bbox = maskUtils.toBbox(rle)

        # Площадь сегментации
        area = maskUtils.area(rle)

        # Добавляем аннотацию в COCO
        coco['annotations'].append({
            "id": annotation_id,
            "image_id": image_id,
            "category_id": class_id + 1,
            "segmentation": rle,
            "area": float(area),
            "bbox": bbox.tolist(),
            "iscrowd": 0,
        })

        annotation_id += 1

# Сохранение в файл COCO
with open(output_json, 'w') as outfile:
    json.dump(coco, outfile, indent=4)

print(f"Конвертация завершена! Аннотации сохранены в {output_json}")