# Открываем файл в режиме чтения
with open('/home/angelika/Downloads/data_bags/Train.txt', 'r') as file:
    # Читаем содержимое файла
    filedata = file.read()

# Заменяем 'data' на 'labels'
newdata = filedata.replace('labels/', '')

# Открываем файл в режиме записи
with open('/home/angelika/Downloads/data_bags/Train.txt', 'w') as file:
    # Записываем новые данные в файл
    file.write(newdata)