import os
import shutil
from sklearn.model_selection import train_test_split

def create_dirs(base_path):
    # Создание подкаталогов train и val
    train_path = os.path.join(base_path, 'train')
    val_path = os.path.join(base_path, 'val')
    
    for sub_dir in ['labels', 'data']:
        os.makedirs(os.path.join(train_path, sub_dir), exist_ok=True)
        os.makedirs(os.path.join(val_path, sub_dir), exist_ok=True)

def move_files(files, source_folder, target_folder):
    for file in files:
        src = os.path.join(source_folder, file)
        dst = os.path.join(target_folder, file)
        shutil.copy(src, dst)

def split_data(data_folder, labels_folder, output_folder, test_size=0.2, random_state=42):
    # Получаем списки файлов изображений (png) и аннотаций (txt)
    images = sorted([f for f in os.listdir(data_folder) if f.endswith('.png')])
    labels = sorted([f for f in os.listdir(labels_folder) if f.endswith('.txt')])
    
    # Убедимся, что количество изображений и аннотаций совпадает
    assert len(images) == len(labels), "Количество изображений и аннотаций должно совпадать."
    
    # Разделяем на тренировочные и валидационные наборы
    train_images, val_images, train_labels, val_labels = train_test_split(
        images, labels, test_size=test_size, random_state=random_state)
    
    # Создание подкаталогов для train и val
    create_dirs(output_folder)

    # Копируем файлы в соответствующие каталоги
    move_files(train_images, data_folder, os.path.join(output_folder, 'train', 'data'))
    move_files(val_images, data_folder, os.path.join(output_folder, 'val', 'data'))
    move_files(train_labels, labels_folder, os.path.join(output_folder, 'train', 'labels'))
    move_files(val_labels, labels_folder, os.path.join(output_folder, 'val', 'labels'))

if __name__ == "__main__":
    # Путь к папкам с исходными данными
    labels_folder =  '/home/angelika/Downloads/finish_fish/labels'
    data_folder =  '/home/angelika/Downloads/finish_fish/data'
    
    # Папка, куда будут сохранены результаты разделения
    output_folder =  '/home/angelika/Downloads/finish_fish/new_data'
    
    # Разделение данных
    split_data(data_folder, labels_folder, output_folder)
