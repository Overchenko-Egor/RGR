import logging # эта библиотека идет вместе с python
from aiogram import Bot, Dispatcher, executor, types # импортируем aiogram

import find as fd
import start as st

import requests
from bs4 import BeautifulSoup as bs

from transliterate import translit
import json
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()
API_TOKEN = '6086335526:AAFCFqJGHugQAZ-PJPcFkTKoHBh1MYsJTjg' # Токен 
logging.basicConfig(level=logging.INFO) # Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage) 
URL_main = "https://www.drom.ru/"


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	st.start()
	

@dp.message_handler(commands='find', state = None)
async def Find(message:  types.Message):
	await fd.FSMFind.model.set()
	await message.answer("Введите марку авто")
	

@dp.message_handler(commands=['favourites'])
async def Favourites(message: types.Message):
	await message.answer("Избранные объявления")
	
@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

fd.register_handler(dp)






if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)