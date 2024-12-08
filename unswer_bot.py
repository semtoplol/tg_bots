import telebot
import random

bot = telebot.TeleBot("7892058221:AAEV5WNosRtvUoVt3QFzCA30wcZsuVeerIc")


@bot.message_handler(commands=['start', 'help'])
def answer_letters(message):
    print("старт")
    bot.send_message(message.chat.id, "Привет, я бот ответчик!")
    bot.reply_to(message, "Я умею отвечать на любой твой вопрос")


@bot.message_handler(commands=['info'])
def answer_make_bot(message):
    bot.send_message(message.chat.id, 'Я был создан 6 октября 2024 года')


@bot.message_handler(content_types=['text'])
def answer_text(message):
    answers = ['да', 'нет', 'может', 'фу', 'осуждаю']
    bot.send_message(message.chat.id, random.choice(answers))


bot.infinity_polling()
