import pandas as pd
import json
import os
import sys
class StudentAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.studentSlowar = {}
        try:
            # Пытаемся загрузить данные из Excel
            self.data = pd.read_excel(file_path)
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            self.data = None  # Если ошибка

    def analiz(self):
        if self.data is None:
            print("Данные не загружены, завершение работы.")
            return 0

        count = 0
        try:
            # Проверяем, существует ли столбец
            if 'Average score' not in self.data.columns:
                print("Столбец 'Average score' не найден.")
                return 0

            # Преобразуем столбец Average score в числовой формат
            self.data['Average score'] = pd.to_numeric(self.data['Average score'], errors='coerce')

            # Фильтруем строки, где Average score не является NaN
            for index, row in self.data.iterrows():
                score = row['Average score']
                fio = row['FIO']
                if pd.notna(score) and score < 4 and score != 0:
                    self.studentSlowar[fio] = 2 #очевидно же что у всех кто там будет будет 2,
                    # если вывод будет три как в таблице это будет странно ведь работа идет с 5- и бальной системой
                    count += 1

            # Сохраняем данные в джейсон
            if hasattr(sys, '_MEIPASS'):
                BASE_DIR = sys._MEIPASS  # Когда код запущен из exe
            else:
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Обычный запуск

            # Формируем путь для сохранения JSON
            json_file_path = os.path.join(BASE_DIR, 'Myscript', 'studentSlowar.json')

            # Сохраняем в файл
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.studentSlowar, f, ensure_ascii=False, indent=4)

            print(f"Количество студентов с оценкой ниже 3: {count}")
            return count

        except Exception as e:
            print(f"Ошибка при анализе данных: {e}")
            return 0
