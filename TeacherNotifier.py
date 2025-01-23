class TeacherNotifier:
    def __init__(self, bot):
        """
        Конструктор класса для уведомления преподавателей.
        :param bot: экземпляр объекта TeleBot для отправки сообщений.
        """
        self.bot = bot
        # Список преподавателей: {"ФИО": Telegram ID}
        self.teachers = {
            "Чернова Юлия": 1973684738,

            # реальный Telegram ID преподавателя
            # Добавьте других преподавателей по мере необходимости
        }

    def add_teacher(self, name, telegram_id):
        """
        Добавить нового преподавателя в список.
        :param name: ФИО преподавателя.
        :param telegram_id: Telegram ID преподавателя.
        """
        self.teachers[name] = telegram_id

    def notify_teachers(self, teachers_with_low_percentage, teachers_not_sending_assignments):
        """
        Уведомляет преподавателей с низким процентом выполнения и тех, кто не отправляет домашние задания.
        :param teachers_with_low_percentage: список кортежей (ФИО, процент).
        :param teachers_not_sending_assignments: список ФИО преподавателей, не отправляющих домашние задания.
        """
        # Уведомление учителей с низким процентом выполнения
        for name, percentage in teachers_with_low_percentage:
            if name in self.teachers:
                telegram_id = self.teachers[name]
                message = (
                    f"Уважаемый(ая) {name}, у вас процент проверки домашних заданий: {percentage:.2f}%. "
                    f"Просьба проверить больше домашних заданий, так как процент ниже 75%."
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

