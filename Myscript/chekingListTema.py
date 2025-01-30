import pandas as pd

file_path = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по темам занятий.xls'

# Загружаем данные из файла
data = pd.read_excel(file_path)

# Выводим список названий столбцов
print("Названия столбцов:", data.columns.tolist())

import pandas as pd

# Загрузка файла
file_path = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по темам занятий.xls'
df = pd.read_excel(file_path)

# Вывод первых строк для всех столбцов
print(df.head())

import pandas as pd

# Путь к файлу
file_path = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по темам занятий.xls'

# Читаем данные из файла
df = pd.read_excel(file_path)

# Выводим первые 10 строк всех столбцов
print(df.head(10).to_string())
