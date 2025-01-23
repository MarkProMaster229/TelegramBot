import telebot
import pandas as pd
from studentsGrups import studentsGrups
from personalaccount import personalaccount
from TeacherNotifier import TeacherNotifier
from TopicCheck import TopicCheck  # Импортируем класс TopicCheck
from TeacherNotifier import TeacherNotifier
from AttendanceAnalyzer import AttendanceAnalyzer
from AttendanceAnalyzer import EmailSender

def mainRealization():
    chatBot = studentsGrups('7576176164:AAHwRUHD2sr8CVg5lW52bC0bNLElkhjXcvU')
    account_manager = personalaccount()  # Создаем экземпляр personalaccount
    teacher_notifier = TeacherNotifier(chatBot.bot)  # Создаем объект TeacherNotifier

    # Глобальная переменная для хранения преподавателей с низким процентом проверки
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

    # Команда для анализа процента проверки
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
            # Прочитайте столбцы с данными из Excel
            provereno_значение = read['Unnamed: 5'].values
            plane_значение = read['Unnamed: 6'].values

            # Цикл, который проверяет процент выполнения
            teachers_with_low_percentage = []
            result_list = []

            for i in range(len(teacher_names)):
                teacher = teacher_names[i]
                provereno = provereno_значение[i]  # правильная переменная
                plan = plane_значение[i]  # правильная переменная

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
            response = "Список преподавателей и пар:\n" + "\n".join(result_list)

            chatBot.bot.send_message(message.chat.id, response)

            if result_list:
                response = "\nПреподаватели с процентом менее 70%:\n" + "\n".join(result_list)
            else:
                response = "\nНет преподавателей с процентом менее 70%."

            chatBot.bot.send_message(message.chat.id, response)

        except Exception as e:
            chatBot.bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

    # Команда для анализа процента выдачи домашних заданий
    @chatBot.bot.message_handler(commands=['assignment_issuance'])
    def assignment_issuance(message):
        try:
            # Указываем столбцы, которые используются для анализа выдачи домашних заданий
            column_teacher_name = 'ФИО преподавателя'  # Название столбца с именами преподавателей
            column_assignments_given = 'Unnamed: 3'  # Название столбца с количеством выданных заданий
            column_assignments_total = 'Unnamed: 6'  # Название столбца с общим количеством заданий

            # Загружаем данные
            file_path = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по домашним заданиям.xlsx'
            data = pd.read_excel(file_path)

            # Проверяем наличие нужных столбцов
            if column_teacher_name not in data.columns or column_assignments_given not in data.columns or column_assignments_total not in data.columns:
                raise ValueError("Не найдены указанные столбцы в файле.")

            # Очищаем и готовим данные
            data = data.dropna(subset=[column_teacher_name])  # Удаляем строки без имен преподавателей
            data[column_assignments_given] = pd.to_numeric(data[column_assignments_given], errors='coerce').fillna(0)
            data[column_assignments_total] = pd.to_numeric(data[column_assignments_total], errors='coerce').fillna(0)

            # Анализ данных для выдачи домашних заданий
            teachers_with_low_assignment_percentage = []
            teachers_not_sending_assignments = []

            for _, row in data.iterrows():
                teacher_name = row[column_teacher_name]
                given = row[column_assignments_given]
                total = row[column_assignments_total]

                if total > 0:
                    percentage = (given / total) * 100
                    if percentage < 70:
                        teachers_with_low_assignment_percentage.append((teacher_name, percentage))
                else:
                    teachers_not_sending_assignments.append(teacher_name)

            # Формируем ответ для выдачи домашних заданий
            response = ""
            if teachers_with_low_assignment_percentage:
                response += "Преподаватели с выдачей менее 70% заданий:\n"
                response += "\n".join(
                    f"{teacher}: {percentage:.2f}%" for teacher, percentage in teachers_with_low_assignment_percentage
                )
            if teachers_not_sending_assignments:
                response += "\nПреподаватели, не выдающие домашние задания:\n"
                response += "\n".join(teachers_not_sending_assignments)

            # Если список пуст
            if not response:
                response = "Все преподаватели выдали домашние задания в необходимом объеме."

            chatBot.bot.send_message(message.chat.id, response)

            # Уведомляем учителей
            notifier = TeacherNotifier(chatBot.bot)
            notifier.notify_teachers(teachers_with_low_assignment_percentage, teachers_not_sending_assignments)

        except Exception as e:
            chatBot.bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

    # Команда для рассылки уведомлений преподавателям
    @chatBot.bot.message_handler(commands=['notify'])
    def notify_teachers_command(message):
        global teachers_with_low_percentage
        try:
            # Если список пустой, пересчитываем его
            if not teachers_with_low_percentage:
                # Загружаем данные для анализа
                file_path = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по домашним заданиям.xlsx'
                read = pd.read_excel(file_path)

                # Проверяем наличие нужных столбцов
                if 'ФИО преподавателя' not in read.columns or 'Unnamed: 5' not in read.columns or 'Unnamed: 6' not in read.columns:
                    raise ValueError("Отсутствуют нужные столбцы в файле.")

                # Очищаем данные
                read = read.dropna(subset=['ФИО преподавателя'])
                read['Unnamed: 5'] = pd.to_numeric(read['Unnamed: 5'], errors='coerce').fillna(0)
                read['Unnamed: 6'] = pd.to_numeric(read['Unnamed: 6'], errors='coerce').fillna(0)

                # Пересчитываем процент проверки
                teachers_with_low_percentage = []
                teacher_names = read['ФИО преподавателя'].values
                provereno_значение = read['Unnamed: 5'].values
                plane_значение = read['Unnamed: 6'].values

                for i in range(len(teacher_names)):
                    teacher = teacher_names[i]
                    provereno = provereno_значение[i]
                    plan = plane_значение[i]

                    if plan > 0:
                        percentage = (provereno / plan) * 100
                        if percentage < 75:
                            teachers_with_low_percentage.append((teacher, percentage))

            # Если после анализа список все еще пуст
            if not teachers_with_low_percentage:
                chatBot.bot.send_message(message.chat.id, "Нет преподавателей для уведомления.")
            else:
                # Отправляем уведомления
                teacher_notifier.notify_teachers(teachers_with_low_percentage, [])
                chatBot.bot.send_message(message.chat.id, "Уведомления успешно отправлены преподавателям.")

        except Exception as e:
            chatBot.bot.send_message(message.chat.id, f"Ошибка при отправке уведомлений: {str(e)}")

    @chatBot.bot.message_handler(commands=['teacherDZ'])
    def teacher_dz(message):
        try:
            # Создаем экземпляр класса TopicCheck и вызываем метод topic
            topic_checker = TopicCheck()
            topic_checker.topic()  # Вызов метода для отправки уведомлений
            chatBot.bot.send_message(message.chat.id, "Уведомления преподавателям успешно отправлены.")
        except Exception as e:
            chatBot.bot.send_message(message.chat.id, f"Ошибка при отправке уведомлений: {str(e)}")

    def otpravka():
        try:
            # Параметры
            file_path = 'C:\\Users\\chelovek\\Desktop\\run\\Отчет по посещаемости студентов.xlsx'
            to_email = "romtomgmai@gmail.com"  # Почта учебной части
            subject = "Отчет о низкой посещаемости групп"
            from_email = "your_email@example.com"  # Почта отправителя
            from_password = "your_password"  # Пароль отправителя

            # Создание объектов
            analyzer = AttendanceAnalyzer(file_path)
            email_sender = EmailSender(from_email, from_password)

            # Анализ посещаемости
            low_attendance = analyzer.analyze()

            if low_attendance.empty:
                print("Все группы имеют посещаемость выше установленного порога.")
                return

            # Формирование текста сообщения
            message_body = "Группы с низкой посещаемостью:\n\n"
            for _, row in low_attendance.iterrows():
                message_body += (
                    f"Преподаватель: {row['ФИО преподавателя']}\n"
                    f"Группа: {row['Группа']}\n"
                    f"Процент посещаемости: {row['Процент посещаемости']}%\n\n"
                )

            # Отправка сообщения
            email_sender.send_email(to_email, subject, message_body)

        except Exception as e:
            print(f"Ошибка: {e}")

    # Начинаем работу бота
    chatBot.bot.polling(none_stop=True)


if __name__ == "__main__":
    mainRealization()
    otpravka()
