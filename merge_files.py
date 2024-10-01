import os

# Путь к папкам с аннотациями
base_labels_dir = '/home/angelika/Downloads/data_bags/labels'
person_labels_dir = '/home/angelika/Downloads/person1/labels'

# Папка для сохранения объединенных аннотаций
output_labels_dir = '/home/angelika/Downloads/merged_labels'
os.makedirs(output_labels_dir, exist_ok=True)

# Получаем список файлов из первой папки
base_files = [f for f in os.listdir(base_labels_dir) if f.endswith('.txt')]

for base_file in base_files:
    base_path = os.path.join(base_labels_dir, base_file)
    person_path = os.path.join(person_labels_dir, base_file)

    # Путь для сохранения объединенного файла
    output_path = os.path.join(output_labels_dir, base_file)

    with open(output_path, 'w') as outfile:
        # Копируем содержимое из базовой папки
        with open(base_path, 'r') as infile:
            outfile.write(infile.read())
        
        # Если есть файл с аннотациями для второго класса, добавляем его содержимое
        if os.path.exists(person_path):
            with open(person_path, 'r') as infile:
                outfile.write(infile.read())

print("Аннотации успешно объединены!")
