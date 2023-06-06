from aiogram import types, Dispatcher
import requests
from bs4 import BeautifulSoup as bs

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

# from find import pars
import find as fd

# ЦЕНА - ПРОБЕГ
async def first(message, state):
    last_message = await message.answer("Ваш запрос обрабатывается...")
    await fd.pars(message, state)
    await last_message.delete()
    price = []
    mileage = []
    for url in fd.href_car:
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        price.append(soup.find('div', class_ = 'css-eazmxc e162wx9x0').get_text())
        mileage.append(soup.find('span', class_ = 'css-1osyw3j ei6iaw00').get_text())

    for i in range(len(price)):
        price[i] = price[i].replace("\xa0", "").replace("₽", "")
        mileage[i] = mileage[i].replace("\xa0", "")

    print(mileage)
    print(price)

    global k
    k = []
    for i in range(len(price)):
        k.append(int(price[i]) / int(mileage[i]))
    print(k)


async def second():
    dxf = 6

async def third():
    dxt = 6