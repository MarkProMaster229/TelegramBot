class TeacherNotifier:
    def __init__(self, bot):

        self.bot = bot
        # Список преподавателей: {"ФИО": Telegram ID}
        self.teachers = {
            "Чернова Юлия": 1973684738,
            #сюда установить id преподавателя
        }

    def add_teacher(self, name, telegram_id):

        self.teachers[name] = telegram_id

    def notify_teachers(self, teachers_with_low_percentage, teachers_not_sending_assignments):


        # Уведомление учителей с низким процентом выполнения
        for name, percentage in teachers_with_low_percentage:
            if name in self.teachers:
                telegram_id = self.teachers[name]
                message = (
                    f"Уважаемый(ая) {name}, ваш процент заданий: {percentage:.2f}%. "
                    f"Просьба исправить ситуацию в ближайщее время."
                )
                self.bot.send_message(telegram_id, message)
            else:
                print(f"Преподаватель {name} не найден в списке для уведомлений.")

        # Уведомление учителей, не отправляющих домашние задания
        for name in teachers_not_sending_assignments:
            if name in self.teachers:
                telegram_id = self.teachers[name]
                message = (
                    f"Уважаемый(ая) {name}, вы не отправили домашние задания своим ученикам. "
                    f"Пожалуйста, проверьте и отправьте задания как можно скорее."
                )
                self.bot.send_message(telegram_id, message)
            else:
                print(f"Преподаватель {name} не найден в списке для уведомлений.")

