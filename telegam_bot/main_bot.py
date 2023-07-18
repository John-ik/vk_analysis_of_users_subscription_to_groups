from telebot import TeleBot, types
from config import bot_token

def main():
    bot = TeleBot(bot_token)

    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        help_markup = types.InlineKeyboardMarkup(row_width=1)
        git_hub_project = types.InlineKeyboardButton("Открыть репозиторий проекта",
                                                     url="https://github.com/Ifanfomin/vk_analysis_of_users_subscription_to_groups")
        show_groups = types.InlineKeyboardButton("Показать группы в базе", callback_data="Группы")
        help_markup.add(git_hub_project, show_groups)
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=help_markup)

    @bot.callback_query_handler(func=lambda call: True)
    def Inline_Handler(call):
        call_data = call.data
        if call_data == "Группы":
            print("Тут вызываем класс для получения групп.")


    @bot.message_handler(content_types=['text'])
    def send_help(message):
        bot.send_message(message.chat.id, 'Для начала работы введи /start')

    bot.infinity_polling()

if __name__ == "__main__":
    main()
