import logging # эта библиотека идет вместе с python
from aiogram import Bot, Dispatcher, executor, types # импортируем aiogram

import requests
from bs4 import BeautifulSoup as bs

headers = {'Accept-Encoding':' gzip, deflate', 'User-Agent': 'python-requests/2.4.2 CPython/3.7.3 Windows/10', 'Content-type': 'application/json', 'Accept': 'text/plain'}
 
resp = req.get(url,  headers=headers, verify=False)
 
j=resp.json()

API_TOKEN = '6086335526:AAFCFqJGHugQAZ-PJPcFkTKoHBh1MYsJTjg' # Токен 
logging.basicConfig(level=logging.INFO) # Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	r = requests.get("https://auto.drom.ru")
	soup = bs(r.text, 'htmm.parser')
	models_car = soup.find_all('a', class_='css-1q66we5 e4ojbx43')
	await message.reply(models_car) # отвечает на сообщение
	

@dp.message_handler(commands=['find'])
async def send_welcome(message: types.Message):
	await message.answer("Поиск обявлений")

@dp.message_handler(commands=['favourites'])
async def send_welcome(message: types.Message):
	await message.answer("Избранные объявления")
	

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)