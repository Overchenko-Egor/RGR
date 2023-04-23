import logging # эта библиотека идет вместе с python
from aiogram import Bot, Dispatcher, executor, types # импортируем aiogram

API_TOKEN = '6086335526:AAFCFqJGHugQAZ-PJPcFkTKoHBh1MYsJTjg' # Токен 
logginglogging.basicConfig(level=logging.INFO) # Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	await message.reply("Привет! Это простейший бот на aiogram") # отвечает на сообщение

	@dp.message_handler()
async def echo(message: types.Message):
	await message.answer(message.text)

	if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
