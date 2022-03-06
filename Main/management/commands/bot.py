import os

import telebot
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from telebot.types import Message

from Main.models import UserInfo

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))


@bot.message_handler(commands=["start"])
def do_action(message: Message):
    bot.send_message(
        message.chat.id,
        "Привет! Я тут чтобы помогать!\n/register - зарегистрироваться в сервисе\nБольше команд нет:(",
    )


@bot.message_handler(commands=["register"])
def register(message: Message):
    username = message.from_user.username
    if username == "" or message.from_user.username is None:
        bot.send_message(
            message.chat.id, "Добавть имя пользователя к своему телеграм аккаунту"
        )
        return
    ui = UserInfo.objects.filter(telegram_chat_id=message.chat.id).first()
    if ui:
        bot.send_message(message.chat.id, "Ты уже зарегистрировался")
        return
    user = User.objects.create(username=username)
    ui = UserInfo.objects.create(user=user, telegram_chat_id=message.chat.id)
    name = message.from_user.first_name
    surname = message.from_user.last_name
    if surname is None or surname == "" or name is None or name == "":
        bot.send_message(
            message.chat.id,
            "Приветствую в Sprint! Сейчас я помогу тебе создать аккаунт.\nДля начала отправь мне свою фамилию",
        )
    else:
        ui.surname = surname
        ui.name = name
        ui.verified = True
        ui.save()
        bot.send_message(
            message.chat.id,
            f"Регистрация завершена! Теперь можешь ты можешь войти в сервис под именем пользователя: {user.username}",
        )


@bot.message_handler(content_types=["text"])
def do_action(message: Message):
    user = User.objects.filter(userinfo__telegram_chat_id=message.chat.id).first()
    if not user:
        bot.send_message(
            message.chat.id,
            "Зарегистрируйся в сервисе, чтобы взаимодействовать со мной",
        )
        return
    if user.userinfo.surname is None:
        user.userinfo.surname = message.text
        user.userinfo.save()
        bot.send_message(message.chat.id, "Отлично! Теперь отправь мне свое имя")
    elif user.userinfo.name is None:
        user.userinfo.name = message.text
        user.userinfo.verified = True
        user.userinfo.save()
        bot.send_message(
            message.chat.id,
            f"Регистрация завершена! Теперь можешь ты можешь войти в сервис под именем пользователя: {user.username}",
        )
    else:
        bot.send_message(message.chat.id, "Я пока больше ничего не умею")


class Command(BaseCommand):
    help = "starts bot"

    def handle(self, *args, **options):
        print("bot is starting")
        bot.polling()
        print("bot failed")
