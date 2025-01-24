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

    def analyze_grades(self, threshold=3):
        try:
            # Проверяем наличие необходимых столбцов
            required_columns = ['FIO', 'Average score']
            for column in required_columns:
                if column not in self.data.columns:
                    raise ValueError(f"Отсутствует столбец '{column}' в файле.")

            # Преобразуем столбец "Average score" к числовому формату
            self.data['Average score'] = pd.to_numeric(self.data['Average score'], errors='coerce').fillna(0)

            # Отбираем студентов с низким средним баллом
            low_grade_students = self.data[self.data['Average score'] < threshold]

            return low_grade_students
        except Exception as e:
            raise ValueError(f"Ошибка при анализе данных: {str(e)}")
