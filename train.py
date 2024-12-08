import telebot
import random

bot = telebot.TeleBot("7896906891:AAGtbjmLKy4Qh2ev3lRUbjsmusH-NIoQk8U")


@bot.message_handler(commands=['start', 'help'])
def answer_letters(message):
    bot.send_message(message.chat.id, "Привет, я твой тернер!")
    bot.reply_to(message, "Я умею поддержать тебя по тренеровкам")


@bot.message_handler(commands=['into'])
def answer_make_bot(message):
    bot.send_message(message.chat.id, 'Я был создан 10 октября 2024 года')


@bot.message_handler(content_types=['text'])
def answer_text(message):
    answers = ['отдыхай', 'еще раз', 'добавить?', 'легенда', 'мало', 'this is so much!', 'щас помогу', 'маловато', 'постарайся ещё']
    bot.send_message(message.chat.id, random.choice(answers))



bot.infinity_polling()