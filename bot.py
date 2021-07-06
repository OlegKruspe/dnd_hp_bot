# -*- coding: utf-8 -*-

import telebot
import keys as k
import db as db

#vars
TOKEN = "1848959216:AAE2_o2qQS5q5Vik8klJFnwNATp1WCKOOIs"
bot = telebot.TeleBot(TOKEN)

#messages
hello_msg = 'Приветствую, приключенец. Я постараюсь помочь тебе в путешествии, считая твои HP. Для начала сообщи мне, каков твой максимальный HP?'
hello_error_msg = 'Прости, HP - это число. Введи, пожалуйста, число.'
hello_success_msg = 'Отлично, я запомнил. Удачного путешествия!'

damage_msg = 'И каков урон?'
heal_msg = 'Насколько полечили?'
rest_msg = 'Отлично, максимальный HP восстановлен.'
change_msg = 'Каков теперь твой макс. HP?'
error_msg = 'Я тебя не понимаю. Попробуй воспользоваться кнопками.'
hpinfo_msg = 'Твой текущий HP - '

@bot.message_handler(commands=['start'])
#Выполняется при нажатии 'start' в чате с ботом
def start_handler(message):
    userid = message.chat.id
    if not db.check(userid):
        msg = bot.send_message(message.from_user.id, hello_msg)
        bot.register_next_step_handler(msg, askFullhp)
    else:
        info = db.ask(userid);
        hp_now = info[1];
        hp_full = info[2];
        msg = bot.send_message(message.from_user.id, hpinfo_msg + str(hp_now))
        bot.register_next_step_handler(msg, askAction)
    
#Бот спрашивает фулл хп
def askFullhp(message):
    userid = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(userid, hello_error_msg)
        bot.register_next_step_handler(msg, askFullhp)
        return
    hp_full = int(message.text)
    db.init(userid, hp_full);
    msg = bot.send_message(userid, hello_success_msg, reply_markup = k.action_markup)
    bot.register_next_step_handler(msg, askAction)

#Бот ждет указаний
def askAction(message):
    userid = message.chat.id
    action = message.text
    if action == 'Меня ранили':
        msg = bot.send_message(userid, damage_msg)
        bot.register_next_step_handler(msg, askDamage)
    elif action == 'Меня полечили':
        msg = bot.send_message(userid, heal_msg)
        bot.register_next_step_handler(msg, askHeal)
    elif action == 'Длинный отдых':
        msg = bot.send_message(userid, rest_msg)
        info = db.ask(userid);
        hp_full = info[2];
        hp_now = hp_full;
        db.write(userid, 'hp_now', hp_now);
        bot.register_next_step_handler(msg, askAction)
    elif action == 'Изменение макс. HP':
        msg = bot.send_message(userid, change_msg)
        bot.register_next_step_handler(msg, askChange)
    else:
        msg = bot.send_message(userid, error_msg)
        bot.register_next_step_handler(msg, askAction)

def askDamage(message):
    userid = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(userid, hello_error_msg)
        bot.register_next_step_handler(msg, askDamage)
        return
    info = db.ask(userid);
    hp_now = info[1];
    hp_now = hp_now - int(message.text);
    if hp_now < 0:
        hp_now = 0
    db.write(userid, 'hp_now', hp_now);
    msg = bot.send_message(userid, hpinfo_msg + str(hp_now), reply_markup = k.action_markup)
    bot.register_next_step_handler(msg, askAction)

def askHeal(message):
    userid = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(userid, hello_error_msg)
        bot.register_next_step_handler(msg, askHeal)
        return
    info = db.ask(userid);
    hp_now = info[1];
    hp_full = info[2];
    hp_now = hp_now + int(message.text)
    if hp_now > hp_full:
        hp_now = hp_full
    db.write(userid, 'hp_now', hp_now);
    msg = bot.send_message(userid, hpinfo_msg + str(hp_now), reply_markup = k.action_markup)
    bot.register_next_step_handler(msg, askAction)

def askChange(message):
    userid = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(userid, hello_error_msg)
        bot.register_next_step_handler(msg, askChange)
        return
    info = db.ask(userid);
    hp_now = info[1];
    hp_full = int(message.text)
    db.write(userid, 'hp_full', hp_full);
    if hp_now > hp_full:
        hp_now = hp_full
        db.write(userid, 'hp_now', hp_now)
    msg = bot.send_message(userid, hello_success_msg, reply_markup = k.action_markup)
    bot.register_next_step_handler(msg, askAction)

bot.polling()
