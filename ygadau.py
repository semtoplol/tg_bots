import telebot
import random

bot = telebot.TeleBot('7927912134:AAE4PehqdpixCdq6UnZNVm85mWhdgzbk94s')
game_started = False
game_stop = False
left = None
right = None
center = 0



@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот угадайка!")
    bot.reply_to(message, "Я умею отгадывать числа в заданном диапазоне. Используй /start_game, чтобы начать. ")


@bot.message_handler(commands=['start_game'])
def start_game(message):
    bot.send_message(message.chat.id, ' Игра запущена! Если хочешь остановить игру, то введи /stop')
    bot.send_message(message.chat.id, 'введи левую границу диапазона, а затем правую границу диапазона')
    global game_started, center, game_stop
    game_started = True
    game_stop = False


@bot.message_handler(commands=['stop'])
def stop_game(message):
    bot.send_message(message.chat.id, ' Бот остановлен!')
    global game_started, game_stop, left, right, center
    game_stop = True
    restart()
    game_started = False



@bot.message_handler(content_types=['text'])
def speak(message):
    global game_started, left, right, center
    if left == None:
        left = int(message.text)
        bot.send_message(message.chat.id, 'левая граница диапазона установленна, теперь укажите правую сторону диапазона')
        return

    if right == None:
        if int(message.text) > left:
            right = int(message.text)
            bot.send_message(message.chat.id,'правая граница диапазона установленна')
        elif int(message.text) <= left:
            right = None
            bot.send_message(message.chat.id, 'введите правый диапазон так, чтобы он был больше левого')
            return

    if game_started:
        if message.text == '>':
            left = center + 1
        elif message.text == '<':
            right = center - 1
        elif message.text == '=':
            bot.send_message(message.chat.id, 'Я угадал, ура!')
            restart()
            game_started = False
            return
        center = (left + right) // 2
        bot.send_message(message.chat.id, f"Ваше число {center}?(<,=,>)")


    else:
        bot.send_message(message.chat.id, 'Для запуска воспользуйтесь командой /start_game')


def restart():
    global left, right, center
    left = None
    right = None
    center = 0



bot.infinity_polling()