import logging # эта библиотека идет вместе с python
from aiogram import Bot, Dispatcher, executor, types # импортируем aiogram

import requests
from bs4 import BeautifulSoup as bs

API_TOKEN = '6086335526:AAFCFqJGHugQAZ-PJPcFkTKoHBh1MYsJTjg' # Токен 
logging.basicConfig(level=logging.INFO) # Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	r = requests.get("https://auto.drom.ru")
	soup = bs(r.text, 'html.parser')
	models_car_c = "."
	models_car = soup.find_all('div', class_='css-lahb1a e4ojbx44')
	for a in models_car:
		if len(a) > 0:
			models_car_c += a.find('span', 'css-1kb7l9z e162wx9x0').text
	#models_car += soup.find_all('div', class_='css-pvjszw')
	#models_car += soup.find_all('a', class_='css-1q66we5 e4ojbx43')
	#clear_m_c = [c.text for c in models_car]
	await message.answer(models_car_c)
	print (models_car_c)
	

@dp.message_handler(commands=['find'])
async def send_welcome(message: types.Message):
	await message.answer("Поиск обявлений")

@dp.message_handler(commands=['favourites'])
async def send_welcome(message: types.Message):
	await message.answer("Избранные объявления")
	

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)