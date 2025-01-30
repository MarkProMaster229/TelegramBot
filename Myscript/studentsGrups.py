import telebot
import pandas as pd
import os
import sys

class studentsGrups:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def load_data(self):
        if hasattr(sys, '_MEIPASS'):
            BASE_DIR = sys._MEIPASS  # Когда код запущен из exe
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Обычный запуск

        # Формируем путь к файлу Excel
        file_path = os.path.join(BASE_DIR, 'data', 'Отчет по студентам.xlsx')

        # Загружаем данные
        df = pd.read_excel(file_path)
        return df

        return df

    def start(self, message):
        self.bot.send_message(message.chat.id, 'Привет! доступные команды - /pairs для получения количества пар по группам.')

    def pairs(self, message):
        try:
            df = self.load_data()
            group_pairs = df.groupby('Группа')['pairs in total per month'].first()
            group_pairs = group_pairs.reset_index()
            group_pairs['Аббревиатура'] = group_pairs['Группа'].str.extract(r'-(\D+)-')
            group_pairs = group_pairs.sort_values(by=['Аббревиатура', 'Группа'])
            response = "Количество пар по группам:\n"
            for _, row in group_pairs.iterrows():
                response += f"{row['Группа']} - {row['pairs in total per month']}\n"
            self.bot.send_message(message.chat.id, response)
        except Exception as e:
            self.bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")



    def help_command(self, message):
        self.bot.send_message(message.chat.id, 'Доступные команды:\n/start - начать работу с ботом\n/pairs - вывести количество пар по группам')
