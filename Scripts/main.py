import telebot
from studentsGrups import studentsGrups
from personalaccount import personalaccount

# Словарь для хранения состояний пользователей
user_states = {}


def configure_personal_account_handlers(bot, account_manager):
    """Настраивает команды бота для работы с личным кабинетом."""

    @bot.message_handler(commands=['register'])
    def register(message):
        try:
            user_id = message.chat.id
            if user_states.get(user_id) != "admin":
                bot.send_message(message.chat.id, "Команда доступна только для администратора.")
                return

            msg_parts = message.text.split()
            if len(msg_parts) != 3:
                bot.send_message(message.chat.id, "Используйте формат: /register [логин] [пароль]")
                return

            username, password = msg_parts[1], msg_parts[2]
            result = account_manager.create_account(username, password, "teacher")
            bot.send_message(message.chat.id, result)
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

    @bot.message_handler(commands=['login'])
    def login(message):
        try:
            user_id = message.chat.id
            msg_parts = message.text.split()
            if len(msg_parts) != 3:
                bot.send_message(message.chat.id, "Используйте формат: /login [логин] [пароль]")
                return

            username, password = msg_parts[1], msg_parts[2]
            result = account_manager.authenticate(username, password)

            if result.startswith("Добро пожаловать"):
                user_role = account_manager.get_role(username)
                user_states[user_id] = user_role
                bot.send_message(message.chat.id, f"{result} Вы вошли как {user_role}.")
            else:
                bot.send_message(message.chat.id, result)
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

    @bot.message_handler(commands=['logout'])
    def logout(message):
        try:
            user_id = message.chat.id
            if user_id in user_states:
                del user_states[user_id]
                bot.send_message(message.chat.id, "Вы успешно вышли из аккаунта.")
            else:
                bot.send_message(message.chat.id, "Вы не авторизованы.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {str(e)}")


def mainRealization():
    chatBot = studentsGrups('7576176164:AAHwRUHD2sr8CVg5lW52bC0bNLElkhjXcvU')

    accountManager = personalaccount('accounts.json')

    # Создаём аккаунт администратора, если он ещё не создан
    accounts = accountManager.load_accounts()
    if "Admin" not in accounts:
        accountManager.create_account("Admin", "1234", "admin")

    # Настройка команд для работы с личным кабинетом
    configure_personal_account_handlers(chatBot.bot, accountManager)

    @chatBot.bot.message_handler(commands=['start'])
    def start(message):
        chatBot.start(message)

    @chatBot.bot.message_handler(commands=['pairs'])
    def pairs(message):
        chatBot.pairs(message)

    @chatBot.bot.message_handler(commands=['help'])
    def help_command(message):
        chatBot.help_command(message)

    chatBot.bot.polling(none_stop=True)


if __name__ == "__main__":
    mainRealization()
