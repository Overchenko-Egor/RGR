import first
import logging # эта библиотека идет вместе с python
from aiogram import Bot, Dispatcher, executor, types # импортируем aiogram

import requests
from bs4 import BeautifulSoup as bs

from transliterate import translit


API_TOKEN = '6086335526:AAFCFqJGHugQAZ-PJPcFkTKoHBh1MYsJTjg' # Токен 
logging.basicConfig(level=logging.INFO) # Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def country():
	print ("find_2")
	@dp.message_handler(content_types = ['text'])
	async def Otvet(message: types.Message):
		print("find_3")
		ru_text = message.text.lower()
		name_country = translit(ru_text, language_code='ru', reversed=True)
		print(name_country)
		await message.answer(name_country)

		URL_for_find = ".drom.ru/auto/"
		r = first.requests.get("https://" + name_country + URL_for_find)
		soup = bs(r.text, 'html.parser')
		find_tegs = soup.find_all("div", class_ = "css-l1wt7n e3f4v4l2")
		# print (find_tegs)
		cars_after_find = []
		for items in find_tegs:
			cars_after_find += items.find_all("span")
		clear_c_f = [c.text for c in cars_after_find]
		await message.answer(clear_c_f)