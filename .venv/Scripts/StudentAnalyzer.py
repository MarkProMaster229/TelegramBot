import pandas as pd

class StudentAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        try:
            self.data = pd.read_excel(self.file_path)
            return self.data
        except Exception as e:
            raise ValueError(f"Ошибка при загрузке файла: {str(e)}")

    def convert_to_5_scale(self):
        if 'Average score' not in self.data.columns:
            raise ValueError("Отсутствует столбец 'Average score' для конвертации.")

        # Преобразуем значения '-' в 0 и остальные значения в float
        self.data['Average score'] = self.data['Average score'].apply(lambda x: 0 if x == '-' else float(x))

        # Конвертируем оценки в 5-балльную систему
        def convert_to_5_scale(score):
            if score <= 3:
                return 2
            elif score <= 6:
                return 3
            elif score <= 9:
                return 4
            else:
                return 5

        self.data['Converted Score'] = self.data['Average score'].apply(convert_to_5_scale)

    def analyze_grades(self, threshold=3):
        try:
            # Проверяем наличие необходимых столбцов
            required_columns = ['FIO', 'Converted Score']
            for column in required_columns:
                if column not in self.data.columns:
                    raise ValueError(f"Отсутствует столбец '{column}' в файле.")

            # Отбираем студентов с низким средним баллом
            low_grade_students = self.data[self.data['Converted Score'] < threshold]

            return low_grade_students
        except Exception as e:
            raise ValueError(f"Ошибка при анализе данных: {str(e)}")
