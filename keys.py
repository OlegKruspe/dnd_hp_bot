from telebot import types

action_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
action_markup_btn1 = types.KeyboardButton('Меня ранили')
action_markup_btn2 = types.KeyboardButton('Меня полечили')
action_markup_btn3 = types.KeyboardButton('Длинный отдых')
action_markup_btn4 = types.KeyboardButton('Изменение макс. HP')
action_markup.row(action_markup_btn1, action_markup_btn2)
action_markup.row(action_markup_btn3, action_markup_btn4)