import os.path

import telebot
from telebot import types
import time
import json

bot = telebot.TeleBot("7965604140:AAE1PSb3NR4eEp6FbsOZv2PoAWjye95yTh0")


class Task:
    def __init__(self, name, task_day="", task_time=""):
        self.name = name
        self.task_day = task_day
        self.task_time = task_time
        self.id = time.time()
        print(self.id)


task_list = {

}


def decode_task(dict):
    if dict.get('type') == 'Task':
        t = Task(dict['name'], dict['day'], dict['time'])
        t.id = dict['id']
        return t
    else:
        return dict


def encode_task(task):
    return {'id': task.id, 'name': task.name, 'day': task.task_day, 'time': task.task_time, 'type': 'Task'}


def read_file():
    global task_list
    if os.path.getsize('data_todolist.json') > 0:
        with open('data_todolist.json') as file:
            task_list = json.load(file, object_hook=decode_task)


read_file()


def write_file():
    global task_list
    with open('data_todolist.json', 'w') as file:
        json.dump(task_list, file, default=encode_task)


def emoji_keyboard(task_id):
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    btnsss = []
    for emo in EMOJI:
        json_dict = json.dumps({'do': EMOJI.index(emo), 'id': task_id, 'time': "_", 'day': '_'})
        print(json_dict)
        emo_butten = types.InlineKeyboardButton(emo, callback_data=json_dict)
        btnsss.append(emo_butten)
    keyboard.add(*btnsss)
    return keyboard


EMOJI = ['✅', '❌', '🗓', '🕑']

WEEK_BUTTONS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


def Day_keyboard(new_task_id):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    btns = []
    for day in WEEK_BUTTONS:
        json_dict = json.dumps({"day": WEEK_BUTTONS.index(day), "id": new_task_id, 'time': '_'})
        print(json_dict)
        day_btn = types.InlineKeyboardButton(day, callback_data=json_dict)
        btns.append(day_btn)
    keyboard.add(*btns)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я бот отвечающий за твой список дел')
    task_list[str(message.chat.id)] = []
    print(task_list)
    keyboard = types.ReplyKeyboardMarkup()
    knopka = types.KeyboardButton("кнопка")
    new_task = types.KeyboardButton("новая задача")
    list_work = types.KeyboardButton("список дел")
    keyboard.add(new_task, list_work, knopka)
    bot.send_message(message.chat.id, 'Напиши "новая задача", чтобы добавить задачу.'
                                      '\n Напиши "список дел", чтобы посмотреть список.'
                                      '\n Напиши "кнопка", чтобы кнопка.', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == 'новая задача':
        bot.send_message(message.chat.id, 'введите название задачи:')
        return

    if message.text.lower() == 'кнопка':
        bot.send_message(message.chat.id, 'введите кнопку:')
        return

    if message.text.lower() == 'список дел':
        bot.send_message(message.chat.id, 'ваш список задач:')
        for i, t in enumerate(task_list[str(message.chat.id)]):
            bot.send_message(message.chat.id, f"{i + 1}) {t.name}__{t.task_day}__{t.task_time}",
                             reply_markup=emoji_keyboard(t.id))

        return
    new_task = Task(message.text)
    task_list[str(message.chat.id)].append(new_task)
    write_file()
    bot.send_message(message.chat.id, f"добавлена задача:'{new_task.name}'")
    bot.send_message(message.chat.id, 'выберите день для выполнения задачи', reply_markup=Day_keyboard(new_task.id))
    bot.send_message(message.chat.id, 'теперь выберите время задачи', reply_markup=time_keyboard(new_task.id))


def time_keyboard(new_task_id):
    keyboard = types.InlineKeyboardMarkup(row_width=6)
    btnss = []
    for timer in range(0, 24):
        timer_btn = types.InlineKeyboardButton(f'{timer}:00', callback_data=json.dumps(
            {"time": f'{timer}:00', "id": new_task_id, 'day': '_'}))
        btnss.append(timer_btn)
    keyboard.add(*btnss)
    return keyboard


def Delete_task(chat_id, task_id):
    for t in task_list[str(chat_id)]:
        if t.id == task_id:
            task_list[str(chat_id)].remove(t)


@bot.callback_query_handler(
    func=lambda call: 'do' in json.loads(call.data) and EMOJI[json.loads(call.data)['do']] in EMOJI)
def Do_select(call):
    id = json.loads(call.data)['id']
    do = EMOJI[json.loads(call.data)['do']]
    chat_id = call.message.chat.id
    if do == EMOJI[0]:
        Delete_task(chat_id=call.message.chat.id, task_id=id)
        bot.edit_message_text(f'Задача выполнена ✅', call.message.chat.id, call.message.message_id)
    if do == EMOJI[1]:
        Delete_task(chat_id=call.message.chat.id, task_id=id)
        bot.edit_message_text(f'Задача удалена ❌', call.message.chat.id, call.message.message_id)
    if do == EMOJI[2]:
        bot.edit_message_text(f'Выберите день', call.message.chat.id, call.message.message_id,
                              reply_markup=Day_keyboard(id))
    if do == EMOJI[3]:
        bot.edit_message_text(f'Выберите время', call.message.chat.id, call.message.message_id,
                              reply_markup=time_keyboard(id))


@bot.callback_query_handler(func=lambda call: json.loads(call.data)['time'][-1] == "0")
def timer_select(call):
    print(call.data)
    id = json.loads(call.data)['id']
    for t in task_list[str(call.message.chat.id)]:
        if t.id == id:
            t.task_time = json.loads(call.data)["time"]
            bot.edit_message_text(f'выбрано время: {t.task_time}', call.message.chat.id, call.message.message_id)
    write_file()


@bot.callback_query_handler(func=lambda call: WEEK_BUTTONS[json.loads(call.data)['day']] in WEEK_BUTTONS)
def Day_select(call):
    print(call.data)
    id = json.loads(call.data)['id']
    for d in task_list[str(call.message.chat.id)]:
        if d.id == id:
            d.task_day = WEEK_BUTTONS[json.loads(call.data)['day']]
            bot.edit_message_text(f'выбран день: {d.task_day}', call.message.chat.id, call.message.message_id)
    write_file()


bot.infinity_polling()
