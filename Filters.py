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
        pr = price[i]
        pr = ''.join([char for char in pr if char.isdigit()])
        mil = mileage[i]
        mil = ''.join([char for char in mil if char.isdigit()])
        k.append(int(pr) / int(mil))
    print(k)
    index = 0
    while (len(fd.href_car) != 0) and index < 10:
            max_value = max(k)
            max_index = k.index(max_value)
            await open(fd.href_car[max_index], message)
            fd.href_car.pop(max_index)
            k.pop(max_index)
            index += 1


async def second(message, state):
    global last_message
    last_message = await message.answer("Ваш запрос обрабатывается...")
    await fd.pars(message, state)
    number_of_owners = []
    for url in fd.href_car:
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        clear = soup.find('button', class_ = 'e8vftt60 css-1uu0zmh e104a11t0').get_text()
        clear = ''.join([char for char in clear if char.isdigit()])
        number_of_owners.append(clear)
    print (number_of_owners)
    index = 0
    while (len(fd.href_car) != 0) and index < 10:
            min_value = min(number_of_owners)
            min_index = number_of_owners.index(min_value)
            await open(fd.href_car[min_index], message)
            fd.href_car.pop(min_index)
            number_of_owners.pop(min_index)
            index += 1

async def third(message, state):
    global last_message
    last_message = await message.answer("Ваш запрос обрабатывается...")
    await fd.pars(message, state)
    limitations = []
    get_lim = []
    for url in fd.href_car:
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        get_div = soup.find_all('div', class_ = 'css-13qo6o5 e1mhp2ux0')
        if (len(get_div) > 0):
            get_lim.append (get_div[2])
        else:
            get_lim.append ('0')
    for item in get_lim:
        get_status = item.get_text()
        limitations.append(get_status)
        print (get_status)

    # if (len(get_div) > 0):
    #     get_status = get_div[2]
    #     limitations.append(get_status)
    # else:
    #     get_status = 0
    #     limitations.append(get_status)
    index = 0
    while (len(fd.href_car) != 0) and index < 10:
        if limitations[index] == 'Ограничений не обнаружено':       
            await open(fd.href_car[index], message)
            fd.href_car.pop(index)
            limitations.pop(index)
            index += 1
            print('ok')
        else:
            fd.href_car.pop(index)
            limitations.pop(index)

async def open(url, message):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    div_photo = soup.find('div', class_ = 'css-1wv4onu ed2my592')
    photo = div_photo.find("img")
    image_url = photo["src"]
    image_data = requests.get(image_url).content
    
    teg_info = soup.find("div", class_= 'css-1j8ksy7 eotelyr0')
    info = teg_info.find("span", class_ = 'css-1kb7l9z e162wx9x0')
    if info is not None:
        info = info.text
        info = info.ljust(600)[:600]
        info += '\n' + url
    await message.answer_photo (image_data, caption = info)
   