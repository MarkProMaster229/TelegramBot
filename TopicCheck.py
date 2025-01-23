import telebot
import pandas as pd
import re

class TopicCheck:
    def topic(self):
        # Словарь с Telegram ID преподавателей
        teachers = {
            "Роман": 1973684738,
            # Добавьте других преподавателей по мере необходимости
        }

        # Путь к файлу
        dok = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по темам занятий.xls'

        # Чтение файла
        reader = pd.read_excel(dok)

        # Проверка наличия нужных столбцов
        if 'Тема урока' not in reader.columns or 'ФИО преподавателя' not in reader.columns:
            raise ValueError("Отсутствуют нужные столбцы в файле.")

        # Получаем список тем уроков и имена преподавателей
        tema_name = reader['Тема урока'].values
        name_prepodavatel = reader['ФИО преподавателя'].values

        # Регулярное выражение для проверки строки
        pattern = r'^Урок №\d+\.\s*Тема:\s*.+$'

        # Инициализация бота
        bot = telebot.TeleBot('7576176164:AAHwRUHD2sr8CVg5lW52bC0bNLElkhjXcvU')

        # Проверяем каждую строку
        for i, (tema, prepodavatel) in enumerate(zip(tema_name, name_prepodavatel)):
            if not re.match(pattern, str(tema)):
                # Логируем ошибку
                print(f"Преподаватель {prepodavatel}: Строка {i + 1} неверна: {tema}")

                # Получаем Telegram ID преподавателя
                teacher_id = teachers.get(prepodavatel)

                # Если ID найден, отправляем сообщение
                if teacher_id:
                    message = (
                        f"Уважаемый {prepodavatel}, у вас некорректно заполнена тема урока.\n\n"
                        f"Ошибка в строке {i + 1}: {tema}\n"
                        f"Пожалуйста, проверьте и исправьте."
                    )
                    bot.send_message(teacher_id, message)
                else:
                    # Если ID не найден
                    print(f"ID для преподавателя {prepodavatel} не найден. Уведомление не отправлено.")
            else:
                print(f"Преподаватель {prepodavatel}: Строка {i + 1} верна: {tema}")
