import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd


class AttendanceAnalyzer:
    def __init__(self, file_path, threshold=65):
        self.file_path = file_path
        self.threshold = threshold

    def analyze(self):
        try:
            # Загружаем данные из Excel
            data = pd.read_excel(self.file_path)

            # Проверяем наличие нужных столбцов
            required_columns = ['ФИО преподавателя', 'Средняя посещаемость']
            for col in required_columns:
                if col not in data.columns:
                    raise ValueError(f"Не найден столбец: {col}")

            # Убираем символ '%' из столбца 'Средняя посещаемость' и преобразуем в числовой формат
            data['Средняя посещаемость'] = data['Средняя посещаемость'].replace('%', '', regex=True).astype(float)

            # Фильтруем данные с посещаемостью ниже заданного порога
            low_attendance = data[data['Средняя посещаемость'] < self.threshold]

            return low_attendance

        except Exception as e:
            raise RuntimeError(f"Ошибка анализа посещаемости: {e}")


class EmailSender:
    def __init__(self, from_email, from_password):
        self.from_email = from_email
        self.from_password = from_password

    def send_email(self, to_email, subject, body):
        try:
            # Настраиваем SMTP-сервер для hMailServer
            print("Подключение к SMTP-серверу...")
            server = smtplib.SMTP('localhost', 25)  # Используйте 587, если настроили TLS
            # server.starttls()  # Раскомментируйте, если используете TLS

            # Авторизация
            print(f"Авторизация как {self.from_email}...")
            server.login(self.from_email, self.from_password)

            # Формируем сообщение
            message = MIMEMultipart()
            message['From'] = self.from_email
            message['To'] = to_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            # Отправка
            print("Отправка сообщения...")
            server.send_message(message)
            server.quit()
            print("Сообщение успешно отправлено.")

        except Exception as e:
            raise RuntimeError(f"Ошибка при отправке сообщения: {e}")


def main():
    try:
        # Параметры
        file_path = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по посещаемости студентов.xlsx'
        to_email = "ph3u2@tohru.org"  # Почта учебной части
        subject = "Отчет о посещаемости ниже 65%"
        from_email = "user@localhost"  # Замените на вашу учетную запись в hMailServer
        from_password = "qazwsx123456789Qwqg"  # Замените на ваш пароль для этой учетной записи

        # Создаем объекты классов
        analyzer = AttendanceAnalyzer(file_path)
        email_sender = EmailSender(from_email, from_password)

        # Анализ данных
        low_attendance = analyzer.analyze()

        if low_attendance.empty:
            print("Все преподаватели имеют посещаемость выше установленного порога.")
            return

        # Формируем текст сообщения
        message_body = "Преподаватели с посещаемостью ниже 65%:\n\n"
        for _, row in low_attendance.iterrows():
            message_body += (
                f"Преподаватель: {row['ФИО преподавателя']}\n"
                f"Посещаемость: {row['Средняя посещаемость']}%\n\n"
            )

        # Отправка письма
        email_sender.send_email(to_email, subject, message_body)
        print("Сообщение успешно отправлено в учебную часть.")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
