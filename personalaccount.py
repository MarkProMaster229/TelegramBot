import pandas as pd

class personalaccount:
    def __init__(self):
        self.file_path = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по домашним заданиям.xlsx'

    def admin(self):
        # Загружаем данные из Excel файла
        read = pd.read_excel(self.file_path)

        # Проверяем наличие нужного столбца
        if 'ФИО преподавателя' not in read.columns:
            raise ValueError("Столбец 'ФИО преподавателя' не найден в файле.")

        # Получаем уникальные значения ФИО преподавателей, исключая пустые значения
        difficult = read['ФИО преподавателя'].dropna().unique()

        # Преобразуем значения в строки
        difficult = [str(name) for name in difficult]

        # Возвращаем список преподавателей
        return difficult

    def pars(self):
        read = pd.read_excel(self.file_path)

        # Проверяем столбцы
        print("Список столбцов:", read.columns.tolist())

        if 'Unnamed: 5' not in read.columns:
            raise ValueError("Столбец 'Кол-во пар' не найден в файле.")

        # Получаем данные из столбца "Кол-во пар"
        pairs = read['Unnamed: 5'].dropna().unique()
        print("Уникальные значения 'Кол-во пар':", pairs)

        # Преобразуем значения в строки
        pairs = [str(pair) for pair in pairs]

        # Возвращаем список пар
        return pairs

    def parsplan(self):
        read = pd.read_excel(self.file_path)

        # Проверяем столбцы
        print("Список столбцов:", read.columns.tolist())

        if 'Unnamed: 6' not in read.columns:
            raise ValueError("Столбец 'Кол-во пар' не найден в файле.")

        # Получаем данные из столбца "Кол-во пар"
        pairsPlan = read['Unnamed: 6'].dropna().unique()
        print("план':", pairsPlan)

        # Преобразуем значения в строки
        pairsPlan = [str(pair) for pair in pairsPlan]

        # Возвращаем список пар
        return pairsPlan
