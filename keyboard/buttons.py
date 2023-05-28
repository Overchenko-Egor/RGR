from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

but_find = KeyboardButton('/find')
but_favourites = KeyboardButton('/favourites')

kb_main = ReplyKeyboardMarkup()

kb_main.add(but_favourites).add(but_find)
