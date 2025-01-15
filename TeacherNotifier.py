class TeacherNotifier:
    def __init__(self, bot):
        """
        Конструктор класса для уведомления преподавателей.
        :param bot: экземпляр объекта TeleBot для отправки сообщений.
        """
        self.bot = bot
        # Список преподавателей: {"ФИО": Telegram ID}
        self.teachers = {
            "Чернова Юлия": 1973684738, # реальный Telegram ID преподавателя


        }

    def add_teacher(self, name, telegram_id):
        """
        Добавить нового преподавателя в список.
        :param name: ФИО преподавателя.
        :param telegram_id: Telegram ID преподавателя.
        """
        self.teachers[name] = telegram_id

    def notify_teachers(self, teachers_with_low_percentage):
        """
        Уведомляет преподавателей с низким процентом выполнения.
        :param teachers_with_low_percentage: список кортежей (ФИО, процент).
        """
        for name, percentage in teachers_with_low_percentage:
            if name in self.teachers:
                telegram_id = self.teachers[name]
                message = (
                    f"Уважаемый(ая) {name}, у вас процент проверки домашних заданий: {percentage:.2f}%. "
                    f"Просьба проверить больше домашних заданий, так как процент ниже 70%."
                )
                self.bot.send_message(telegram_id, message)
            else:
                print(f"Преподаватель {name} не найден в списке для уведомлений.")
