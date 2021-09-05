import telebot


bot = telebot.TeleBot("1994460106:AAGrGsCZjF6DVG_T-zycELuVfxnWw8x7UyU")


@bot.message_handler(commands=["start"])
@bot.message_handler(content_types=["text"])
def do_action(message):
    bot.send_message(chat_id=message.chat.id, text=f"ID чата: {message.chat.id}")


if __name__ == '__main__':
    print('bot is starting')
    bot.polling()
    print('bot failed')
