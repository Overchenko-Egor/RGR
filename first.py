import logging # эта библиотека идет вместе с python
from aiogram import Bot, Dispatcher, executor, types # импортируем aiogram

import requests
from bs4 import BeautifulSoup as bs

from transliterate import translit

API_TOKEN = '6086335526:AAFCFqJGHugQAZ-PJPcFkTKoHBh1MYsJTjg' # Токен 
logging.basicConfig(level=logging.INFO) # Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
URL = "https://moscow.drom.ru/auto/"

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	r = requests.get(URL)
	soup = bs(r.text, 'html.parser')
	mc = soup.find_all("a", class_="css-1q66we5 e4ojbx43")
	print (mc)
	clear_m_c = [c.text for c in mc]
	await message.answer(clear_m_c)
	print (clear_m_c)
	

@dp.message_handler(commands=['find'])
async def Find(message:  types.Message):
	await message.answer("Введите населенный пункт")
	country()

@dp.message_handler(commands=['favourites'])
async def Favourites(message: types.Message):
	await message.answer("Избранные объявления")
	




def country():
	@dp.message_handler(content_types = ['text'])
	async def Otvet(message: types.Message):
		# r = requests.get("https://auto.drom.ru")
		# soup = bs(r.text, 'html.parser')
		# country_name = soup.find_all("div", class_="css-7vvcbu edw82zo1")
		# clear_country_name = [c.text for c in country_name]
		# await message.answer (clear_country_name)

		ru_text = message.text.lower()
		text = translit(ru_text, language_code='ru', reversed=True)

		await message.answer(text)




if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)