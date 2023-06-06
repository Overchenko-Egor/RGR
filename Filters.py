from aiogram import Bot, Dispatcher, executor, types # импортируем aiogram
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
    global last_message
    last_message = await message.answer("Ваш запрос обрабатывается...")
    await fd.pars(message, state)
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
    while len(fd.href_car) != 0:
        max_value = max(fd.href_car)
        max_index = fd.href_car.index(max_value)
        await open(fd.href_car[max_index], message)
        fd.href_car.pop(max_index)
    # for i in fd.href_car:
    #     await open(i, message)


async def second():
    dxf = 6

async def third():
    dxt = 6

async def open(url, message):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    # advertisement = soup.find('div', class_ = 'css-1wv4onu ed2my592')
    div_photo = soup.find('div', class_ = 'css-1wv4onu ed2my592')
    photo = div_photo.find("img")
    image_url = photo["src"]
    image_data = requests.get(image_url).content
    
    teg_info = soup.find("div", class_= 'css-1j8ksy7 eotelyr0')
    info = teg_info.find("span", class_ = 'css-1kb7l9z e162wx9x0')
    if info is not None:
        info = info.text
    info = info.ljust(900)[:900]
    info += '\n' + url
    await message.answer_photo (image_data, caption = info)
   