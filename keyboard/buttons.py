from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


but_1 = KeyboardButton('/find')
but_2 = KeyboardButton('1')
but_3 = KeyboardButton('2')
but_4 = KeyboardButton('3')
kb_find = ReplyKeyboardMarkup

kb_find = ReplyKeyboardMarkup().add(but_1)

# kb_find.add(but_1)