import telebot
import pandas as pd
from studentsGrups import studentsGrups
from personalaccount import personalaccount  
from TeacherNotifier import TeacherNotifier

def mainRealization():
    chatBot = studentsGrups('7576176164:AAHwRUHD2sr8CVg5lW52bC0bNLElkhjXcvU')
    account_manager = personalaccount()  # Создаем экземпляр personalaccount
    teacher_notifier = TeacherNotifier(chatBot.bot)  # Создаем объект TeacherNotifier

    # Глобальная переменная для хранения преподавателей с низким процентом
    global teachers_with_low_percentage
    teachers_with_low_percentage = []

    @chatBot.bot.message_handler(commands=['start'])
    def start(message):
        chatBot.start(message)

    @chatBot.bot.message_handler(commands=['pairs'])
    def pairs(message):
        chatBot.pairs(message)

    @chatBot.bot.message_handler(commands=['help'])
    def help_command(message):
        chatBot.help_command(message)

    # Команда для анализа преподавателей
    @chatBot.bot.message_handler(commands=['teachers'])
    def teachers(message):
        global teachers_with_low_percentage
        try:
            # Загружаем данные
            file_path = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по домашним заданиям.xlsx'
            read = pd.read_excel(file_path)

            # Проверка наличия столбцов
            if 'ФИО преподавателя' not in read.columns or 'Unnamed: 5' not in read.columns or 'Unnamed: 6' not in read.columns:
                raise ValueError("Отсутствуют нужные столбцы в файле.")

            # Очистка данных от некорректных значений
            read = read.dropna(subset=['ФИО преподавателя'])  # Удаляем строки без ФИО
            read['Unnamed: 5'] = pd.to_numeric(read['Unnamed: 5'], errors='coerce').fillna(0)  # Преобразуем в числа
            read['Unnamed: 6'] = pd.to_numeric(read['Unnamed: 6'], errors='coerce').fillna(0)  # Преобразуем в числа

            # Получаем данные
            teacher_names = read['ФИО преподавателя'].values
            provereno_znachenie = read['Unnamed: 5'].values
            plane_znachenie = read['Unnamed: 6'].values

            # Список преподавателей и их пар
            teacher_pairs = [
                f"{teacher_names[i]} - {int(provereno_znachenie[i])}" for i in range(len(teacher_names))
            ]

            # Преподаватели с процентом менее 70%
            teachers_with_low_percentage = []
            result_list = []

            for i in range(len(teacher_names)):
                teacher = teacher_names[i]
                provereno = provereno_znachenie[i]
                plan = plane_znachenie[i]

                if plan > 0:
                    percentage = (provereno / plan) * 100
                    if percentage < 70:
                        teachers_with_low_percentage.append((teacher, percentage))
                        result_list.append(f"{teacher}: {percentage:.2f}%")
                    else:
                        result_list.append(f"{teacher}: {percentage:.2f}%")
                else:
                    result_list.append(f"{teacher}: План равен 0, вычисление невозможно")

            # Отправляем общий список
            response = "Список преподавателей и пар:\n" + "\n".join(teacher_pairs)
            chatBot.bot.send_message(message.chat.id, response)

            if result_list:
                response = "\nПреподаватели с процентом менее 70%:\n" + "\n".join(result_list)
            else:
                response = "\nНет преподавателей с процентом менее 70%."

            chatBot.bot.send_message(message.chat.id, response)

        except Exception as e:
            chatBot.bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

    # Команда для рассылки уведомлений преподавателям
    @chatBot.bot.message_handler(commands=['notify'])
    def notify_teachers_command(message):
        global teachers_with_low_percentage
        try:
            if not teachers_with_low_percentage:
                chatBot.bot.send_message(message.chat.id, "Нет преподавателей для уведомления.")
            else:
                teacher_notifier.notify_teachers(teachers_with_low_percentage)
                chatBot.bot.send_message(message.chat.id, "Уведомления успешно отправлены преподавателям.")
        except Exception as e:
            chatBot.bot.send_message(message.chat.id, f"Ошибка при отправке уведомлений: {str(e)}")

    chatBot.bot.polling(none_stop=True)

if __name__ == "__main__":
    mainRealization()
