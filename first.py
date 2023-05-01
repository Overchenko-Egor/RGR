import logging # эта библиотека идет вместе с python
from aiogram import Bot, Dispatcher, executor, types # импортируем aiogram

import requests
from bs4 import BeautifulSoup as bs

from transliterate import translit

API_TOKEN = '6086335526:AAFCFqJGHugQAZ-PJPcFkTKoHBh1MYsJTjg' # Токен 
logging.basicConfig(level=logging.INFO) # Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
URL_main = "https://www.drom.ru/"

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	r = requests.get(URL_main)
	soup = bs(r.text, 'html.parser')
	mc = soup.find_all("a", class_="css-1q66we5 e4ojbx43")
	other_models = soup.find_all("noscript")
	for items in other_models:
		mc += items.find_all("a", href_ = "")
	clear_m_c = [c.text for c in mc]
	await message.answer(clear_m_c)
	

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
		ru_text = message.text.lower()
		name_country = translit(ru_text, language_code='ru', reversed=True)
		
		await message.answer(name_country)

		URL_for_find = ".drom.ru/auto/"
		r = requests.get("https://" + name_country + URL_for_find)
		soup = bs(r.text, 'html.parser')
		find_tegs = soup.find_all("div", class_ = "css-l1wt7n e3f4v4l2")
		# print (find_tegs)
		cars_after_find = []
		for items in find_tegs:
			cars_after_find += items.find_all("span")
		clear_c_f = [c.text for c in cars_after_find]
		await message.answer(clear_c_f)




if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)