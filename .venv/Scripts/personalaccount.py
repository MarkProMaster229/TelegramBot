import pandas as pd

class personalaccount:
    def __init__(self):
        # Укажите путь к вашему Excel файлу
        self.file_path = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по домашним заданиям.xlsx'

    def admin(self):
        """
        Возвращает список уникальных преподавателей из столбца 'ФИО преподавателя'.
        """
        # Загружаем данные из Excel файла
        read = pd.read_excel(self.file_path)

        # Проверяем наличие нужного столбца
        if 'ФИО преподавателя' not in read.columns:
            raise ValueError("Столбец 'ФИО преподавателя' не найден в файле.")

        # Получаем уникальные значения ФИО преподавателей, исключая пустые значения
        difficult = read['ФИО преподавателя'].dropna().unique()

        # Преобразуем значения в строки
        difficult = [str(name) for name in difficult]

        return difficult

    def pars(self):
        """
        Возвращает список уникальных значений из столбца 'Unnamed: 5' (Кол-во пар).
        """
        # Загружаем данные из Excel файла
        read = pd.read_excel(self.file_path)

        # Проверяем наличие столбца
        if 'Unnamed: 5' not in read.columns:
            raise ValueError("Столбец 'Кол-во пар' не найден в файле.")

        # Получаем данные из столбца "Кол-во пар"
        pairs = read['Unnamed: 5'].dropna().unique()

        # Преобразуем значения в строки
        pairs = [str(pair) for pair in pairs]

        return pairs

    def parsplan(self):
        """
        Возвращает список уникальных значений из столбца 'Unnamed: 6' (План).
        """
        # Загружаем данные из Excel файла
        read = pd.read_excel(self.file_path)

        # Проверяем наличие столбца
        if 'Unnamed: 6' not in read.columns:
            raise ValueError("Столбец 'План' не найден в файле.")

        # Получаем данные из столбца "План"
        pairsPlan = read['Unnamed: 6'].dropna().unique()

        # Преобразуем значения в строки
        pairsPlan = [str(pair) for pair in pairsPlan]

        return pairsPlan

    def calculate_assignment_issuance(self):
        """
        Анализирует выдачу заданий и возвращает список преподавателей, у которых процент выдачи
        заданий (выдано / план) меньше 70%.
        """
        try:
            # Загружаем данные из Excel файла
            data = pd.read_excel(self.file_path)

            # Проверяем наличие нужных столбцов
            if 'ФИО преподавателя' not in data.columns or 'Unnamed: 3' not in data.columns or 'Unnamed: 6' not in data.columns:
                raise ValueError("Отсутствуют нужные столбцы для анализа выдачи заданий.")

            # Очистка данных
            data = data.dropna(subset=['ФИО преподавателя'])  # Удаляем строки без ФИО
            data['Unnamed: 3'] = pd.to_numeric(data['Unnamed: 3'], errors='coerce').fillna(0)  # Преобразуем в числа
            data['Unnamed: 6'] = pd.to_numeric(data['Unnamed: 6'], errors='coerce').fillna(0)  # Преобразуем в числа

            # Список преподавателей с низким процентом выдачи заданий
            low_assignment_percentage = []

            for _, row in data.iterrows():
                teacher = row['ФИО преподавателя']
                issued = row['Unnamed: 3']
                planned = row['Unnamed: 6']

                if planned > 0:
                    percentage = (issued / planned) * 100
                    if percentage < 70:
                        low_assignment_percentage.append((teacher, percentage))

            return low_assignment_percentage

        except Exception as e:
            raise Exception(f"Ошибка при анализе выдачи заданий: {str(e)}")

    def get_teachers_not_sending_assignments(self):
        """
        Возвращает список преподавателей, которые не отправляют задания (план равен 0).
        """
        # Загружаем данные из Excel
        read = pd.read_excel(self.file_path)

        # Проверяем наличие нужных столбцов
        if 'ФИО преподавателя' not in read.columns or 'Unnamed: 3' not in read.columns or 'Unnamed: 6' not in read.columns:
            raise ValueError("Отсутствуют нужные столбцы в файле.")

        # Получаем преподавателей, у которых план равен 0
        teachers_not_sending_assignments = read[read['Unnamed: 6'] == 0]['ФИО преподавателя'].dropna().unique()

        return teachers_not_sending_assignments
