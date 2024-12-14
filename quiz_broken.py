import telebot
from telebot import types
import json
import os.path
import random

bot = telebot.TeleBot('7677668515:AAGbn7pZJypPG5-6BIeiSXVPuPeVjv5mnN4')

# текст кнопок
BUTTONS = ["Новая игра 💰", "Статистика 📊"]
# файл с данными пользователя
USER_DATA = "data.json"
# файл со списком всех вопросов
QUESTIONS = "question.json"
# текст ответов бота
ANSWERS_YES = ["👍 Абсолютно верно! 👍", "👏 Вы правы, как никогда! 👏", "👌 Достойный ответ и, к тому же, правильный! 👌"]

# для справки: словарь всех возможных вопросов, 
# ключом является текст вопроса, значением является список вариантов ответов, верный ответ - последний в списке
# этот словарь записан в файл question.json

# questions_dict = {
#  "Какой вид транспорта, еще не имеет службы предварительного заказа билетов?" : ["Морской", "Авиационный", "Железнодорожный", "Троллейбусный"],
#  "Как звали пушкинского Онегина?" : ["Александр", "Иван", "Михаил", "Евгений"],
#  "Кого рыбак всегда видит издалека?" : ["Червяка", "Рыбовода", "Рыбнадзор", "Рыбака"],
#  "Какой из этих этапов истории не имеет соответствующего школьного учебника?" : ["Древний мир", "Средние века", "Новейшая история", "Советская перестройка"],
#  "Через какую папку можно дефрагментировать диск в 95 Windows?" : ["Корзина", "Сетевое окружение", "Мои документы", "Мой компьютер"],
#  "Какое из этих женских имен в переводе с латинского означает 'Победа'?" : ["Олимпиада", "Ноябрина", "Капитолина", "Виктория"],
#  "Чему равен периметр ромба со стороной 2 м?" : ["4 метра", "6 литров", "8 метров квадратных", "8 метров"],
#  "Как называется острая мексиканская приправа?" : ["Сациви", "Пицца", "Лечо", "Чили"],
#  "Что на театральном билете обозначено цифрами?" : ["Размер кресла", "Гардеробный номер", "Очередь в буфет", "Ряд и место"],
#  "Что Пётр I велел брить всем боярам и дворянам?" : ["Косы", "Ноги", "Брови", "Бороды"],
#  "Какое из этих ядер меньше всех остальных?" : ["Пушечное", "Метательное", "Земное", "Атомное"],
#  "Какой строительный материал НЕ входит в состав Пирамиды Хеопса?" : ["Базальт", "Гранит", "Известняк", "Асбест"],
#  "Шкуру какого медведя не принято делить?" : ["Бурого", "Белого", "Плюшевого", "Неубитого"],
#  "Из чего, согласно поговорке не выкинешь слов?" : ["Конституции", "Газеты", "Молитвы", "Песни"],
#  "Чтобы приготовить Колобок, старуха намела..." : ["Снега", "Листьев", "Сена", "Муки"],
#  "В честь чего был назван компьютер компании 'Макинтош'?" : ["Вид плаща", "Зонт", "Населённый пункт", "Сорт яблок"],
#  "Что коллекционирует филуменист?" : ["Фотографии", "Пробки", "Предметы живописи", "Спичечные коробки"],
#  "Название какой монетки происходит от слова 'сто' ?" : ["копейка", "шиллинг", "пфенниг", "цент"],
#  "В какой стране расположена самая высокая гора Британских островов?" : ["Англия", "Уэльс", "Судан", "Шотландия"],
#  "На сколько градусов нужно повернуть циферблат часов, находясь в Англии, чтобы узнать время в Индии?" : ["0", "90", "270", "180"],
#  "Какой вопрос, по определению, не требует ответа?" : ["Каверзный", "Философский", "Экзаменационный", "Риторический"],
#  "Именно в этой стране в 1956 году впервые прошёл ежегодный музыкальный конкурс Евровидение?" : ["Италия", "Франция", "Великобритания", "Швейцария"],
#  "Как называется боязнь глубины?" : ["Таласофобия", "Кимофобия", "Гидрофобия", "Батофобия"],
#  "Назовите самый многочисленный (и по количеству выпущенных игр и по популярности среди пользователей) жанр компьютерных игр." : ["Arcade", "RPG", "RTS", "Action"],
#  "Сколько процентов из жизни ленивцы проводят во сне?" : ["70%", "80%", "85%", "75%"],
#  }

# словарь пользователей
# ключ - id чата
# значение - словарь с данными пользователя: общее количество монет, количество раундов, состояние текущего раунда
users = {}


def decode_round(dict):
    if dict.get('type') == 'Round':
        r = Round()
        r.money = dict.get('money')
        r.questions = dict.get('questions')
        return r
    else:
        return dict


def encode_round(round):
    return {'money': round.money, 'question': round.questions, 'type': round}


# запись общего списка вопросов в файл
def write_file():
    with open(USER_DATA, "w") as file:
        json.dump(users, file, default=encode_round)


def read_user_data():
    global users
    if os.path.getsize(USER_DATA) > 0:
        with open(USER_DATA) as file:
            users = json.load(file, object_hook=decode_round)
            print(users)
            return users


# чтение общего списка вопросов из файла
def read_questions():
    if os.path.getsize(QUESTIONS) > 0:
        with open(QUESTIONS) as file:
            # загружаем json из файла    
            data = json.load(file, object_hook=decode_round)
            print(data)
            return data
    else:
        return {}


read_questions()


# класс для создания нового раунда игры из 6 случайных вопросов
# и хранения состояния текущего раунда: выигрыша игрока и оставшихся вопросов
class Round:
    questions_count = 6

    def __init__(self):
        self.money = 0
        # чтение всех вопросов из файла
        all_questions_dict = read_questions()
        # словарь, в который будут добавлены 6 случайных вопросов для провередния текущего раунда
        self.questions = {}
        for i in range(0, self.questions_count):
            # получем все ключи в виде списка
            keys = list(all_questions_dict.keys())
            # выбираем случайный ключ
            key = random.choice(keys)
            # добавляем вопрос в словарь вопросов для раунда
            self.questions[key] = all_questions_dict.get(key)
            # удаляем элемент из словаря всех вопросов с помощью метода pop,
            # чтобы вопрос не попался в раунде дважды
            all_questions_dict.pop(key)
        # выводим вопросы выбранные для раунда для контроля
        print(self.questions)

        # метод добавления монет игроку за правильный ответ

    def add_money(self):
        if self.money == 0:
            self.money = 10
        else:
            self.money *= 10
        return self.money

    # метод получения следующего вопроса
    def get_question(self):
        # если вопросы еще остались
        if len(self.questions) > 0:
            # метод popitem удаляет последний элемент в словаре и возвращает кортеж из двух элементов: ключа и значения  
            text, answers = self.questions.popitem()
            return text, answers
        # если вопросов не осталось, то возвращаем None и выигранную сумму
        else:
            return None, self.money


# функция создания клавиатуры для управления игрой с кнопками "Новая игра" и "Статистика"
def control_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    new_game_btn = types.InlineKeyboardButton(BUTTONS[0], callback_data=BUTTONS[0])
    stat_game_btn = types.InlineKeyboardButton(BUTTONS[1], callback_data=BUTTONS[1])
    keyboard.row(new_game_btn, stat_game_btn)
    return keyboard


# функция создания клавиатуры с вариантами ответов
def answer_keyboard(answers):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard_buttons = []
    for answer in answers:
        # данные кнопки тип:"ответ", ok: "1", если правильный ответ, "0", если неправильный
        data = {"type": "answer", "ok": "0"}
        # в списке ответов на вопросы правильный ответ всегда последний с индексом 3
        if answers.index(answer) == 3:
            data["ok"] = "1"
        # сохраняем данные в json-строку
        json_string = json.dumps(data)
        # создаем кнопку с текстом ответа и callback_data данными с типом-ответ и указанием верный или неверный ответ
        button = types.InlineKeyboardButton(answer, callback_data=json_string)
        keyboard_buttons.append(button)
    # метод shuffle перемешивает список, чтобы кнопки с вариантами ответов появлялись в случайном порядке
    random.shuffle(keyboard_buttons)
    keyboard.add(*keyboard_buttons)
    return keyboard


# обработчик команды start выводит приветствие и 2 кнопки: "Новая игра" и "Статистика"
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, хочешь стать миллионером? 🤑", reply_markup=control_keyboard())
    global users
    users[str(message.chat.id)] = {}
    write_file()


# обработчик команды help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     "Привет! Вот список доступных команд:"
                     "\n/start - начало работы"
                     "\n/help - список доступных команд")


# получение данных (общая сумма денег, число сыгранных игр и текущий раунд) о пользователе по id чата
def get_user_data(chat_id):
    user = users.get(int(chat_id))
    if user:
        money = user.get("money")
        rounds = user.get("rounds")
        new_round = user.get("new_round")
        return int(money), int(rounds), new_round
    else:
        return 0, 0, Round()
    write_file()


# сохранение данных пользователя (общая сумма денег, число сыгранных игр и текущий раунд) в словарь пользователей по ключу id чата
def set_user_data(chat_id, money, rounds, new_round):
    users[str(chat_id)] = {"money": int(money), "new_round": new_round, "rounds": rounds}
    write_file()
    read_user_data()


# обработчик всех запросов обратного вызова (всех нажатий на встроенные кнопки)
@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    read_user_data()
    # получение данных текущего пользователя: все деньги, количество сыгранных раундов, текущий раунд
    all_money, rounds, new_round = get_user_data(call.message.chat.id)
    # кнопка "Новая игра"
    if call.data == BUTTONS[0]:
        # создаем новый раунд, он будет содержать в себе вопросы
        new_round = Round()
        # получаем вопрос и варианты ответов
        question, answers = new_round.get_question()
        text = (f"Игра началась!"
                f"\n❓ Вопрос на {10} монет:")
        bot.edit_message_text(f"{text}"
                              f"\n{question}", call.message.chat.id, call.message.message_id,
                              reply_markup=answer_keyboard(answers))
    # кнопка "Статистика"
    elif call.data == BUTTONS[1]:
        text = (f"Всего монет: {all_money} 🪙"
                f"\nВсего игр: {rounds} 🎮")
        bot.edit_message_text(f"{text}", call.message.chat.id, call.message.message_id, reply_markup=control_keyboard())
    # кнопки-ответы
    else:
        # загружаем данные, которые пришли с кнопки
        data = json.loads(call.data)
        # получаем тип, если тип "ответ"
        if data.get("type") == "answer":
            # получаем правильный ответ или нет
            ok = data.get("ok")
            # если выбран правильный ответ 
            if ok == "1":
                # добавляем монеты
                money = new_round.add_money()
                all_money += int(money)
                # выводим следующий вопрос
                question, answers = new_round.get_question()
                # если вопросы еще есть, то есть get_question вернул не None, то выводим следующий вопрос
                if question:
                    text = (f"{random.choice(ANSWERS_YES)}\nУ вас {money} монет 🪙"
                            f"\n❓Следующий вопрос на {money * 10} монет:\n")
                    bot.edit_message_text(f"{text}{question}", call.message.chat.id, call.message.message_id,
                                          reply_markup=answer_keyboard(answers))
                # иначе раунд закончен с победой
                else:
                    text = (f"🎁 Поздравляю! Раунд завершен! 🎁"
                            f"\n💵Ваш выигрыш {money} монет:\n")
                    bot.edit_message_text(f"{text}", call.message.chat.id, call.message.message_id,
                                          reply_markup=control_keyboard())
                    # добавляем монеты, количество игр, текущий раунд ставим в None
                    money = new_round.add_money()
                    all_money += int(money)
                    rounds += 1
                    new_round = None
            # если выбран неправильный ответ, то раунд заканчивается проигрышем
            elif ok == "0":
                text = "Вы ошиблись! 😢\nНовый раунд будет лучше..."
                bot.edit_message_text(f"{text}", call.message.chat.id, call.message.message_id,
                                      reply_markup=control_keyboard())
                # добавляем количество игр, текущий раунд ставим в None, деньги не добавляем
                new_round = None
    # сохраняем все данные
    write_file()
    set_user_data(call.message.chat.id, all_money, rounds, new_round)
    bot.answer_callback_query(call.id)


bot.infinity_polling()
