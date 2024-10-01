import os
import glob
import shutil

# путь к вашей директории
path = '/home/angelika/Desktop/cogmodel/bags/rosbag2_2024_09_25-14_36_15/28_08'

# путь к новой директории, куда вы хотите скопировать изображения
new_path = '/home/angelika/Desktop/cogmodel/bags/bags_25_09/past/mini'


# создаем новую директорию, если она не существует
if not os.path.exists(new_path):
    os.makedirs(new_path)

# получаем список всех файлов-изображений
files = glob.glob(os.path.join(path, '*.png'))  # замените '*.jpg' на соответствующий формат ваших изображений
# выбираем каждый 15-й файл
selected_files = files[::40]

# копируем выбранные изображения в новую директорию
for file in selected_files:
    shutil.copy(file, new_path)
