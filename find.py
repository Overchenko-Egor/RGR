from aiogram import types, Dispatcher
import Filters as filter
import requests
from data_base import sqlite
import aiohttp
import json
from transliterate import translit
import sqlite3 as sq
from bs4 import BeautifulSoup as bs

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

Find_URL = ''

storage = MemoryStorage()
# КЛАСС СОСТОЯНИЙ
class FSMFind(StatesGroup):
    model = State()
    full_model = State()
    year = State()
    country = State()
    radius = State()
    search_parameter = State()

# Начало
async def Find(message:  types.Message):
	await FSMFind.model.set()
	await message.answer("Введите марку авто")
	
# Марка
async def model(message: types.Message, state: FSMContext):
    mod = message.text
    if await check_brand(mod):
        await message.answer("Некоректная марка автомобиля. Попробуйте ещё раз!")
        await FSMFind.model.set()
    else:
        async with state.proxy() as date:
            date ['model'] = message.text
        await FSMFind.next()
        await message.answer("Введите модель для подбора авто")

# Модель
async def full_model(message: types.Message, state: FSMContext):
    mod = message.text
    mod = mod.title()
    brand = None
    async with state.proxy() as date:
        brand = date ['model']
    if await ckek_model(mod, brand):
        await message.answer("Некоректная модель автомобиля. Попробуйте ещё раз!")
        await FSMFind.full_model.set()
    else:
        async with state.proxy() as date:
            date ['full_model'] = message.text
        await FSMFind.next()
        await message.answer("Введите год автомобиля \n(Вам будут показаны атвомобили с годом выпуска +1 и -1 от введенного)")

# Год
async def year(message: types.Message, state: FSMContext):
    mod = message.text
    if mod.isdigit():
        async with state.proxy() as date:
            date ['year'] = message.text
        await FSMFind.next()
        await message.answer("Введите город для подбора авто")
    else:
        await message.answer("Введены некорректныеданные. Попробуйте ещё раз!")
        await FSMFind.year.set()

# Город
async def country_find(message:  types.Message, state: FSMContext):
    last_message = await message.answer("Запрос обрабатывается...")
    mod = message.text
    URL_for_find = ".drom.ru/"
    mod = mod.replace("/", "")
    mod = mod.replace("\\", "")
    country_name = await country(URL_for_find, mod)
    flag = await checker(country_name)
    await last_message.delete()
    if (flag):
        async with state.proxy() as date:
            date ['country'] = country_name
            await FSMFind.next()
            await message.answer("Введите радиус поиска") 

    else:
         await message.answer("Город указан не корректно. \nПовторите попытку!")
         await FSMFind.country.set()

    
        
# Радиус
async def radius(message:  types.Message, state: FSMContext):
    async with state.proxy() as date:
        date ['radius'] = message.text
    if message.text.isdigit():
        await FSMFind.next()
        await message.answer("Выберите один из предложенных методов сортировки объявлений\n1 - Цена-пробег\n2 - Количество владельцев\n3 - Наличие ограничений на регистрационные действия")
    else:
        await message.answer("Некорректный формат. \nВы можете ввести только одно целое число без пробелов и знаков препинания! \nПовторите попытку!")
        await FSMFind.radius.set()

# Фильтры
async def search_parameter(message:  types.Message, state: FSMContext):
    mod = message.text
    async with state.proxy() as date:
        date ['search_parameter'] = mod

    last_message = await message.answer("Ваш запрос обрабатывается...")
    await pars(message, state)
    await last_message.delete()
    

async def pars(message:  types.Message, state: FSMContext):
    # ЗАВЕРШЕНИЕ
    global href_car
    href_car = [] 
    name_country = None
    name_radius = None
    name_model = None
    name_full_model = None
    name_year = None
    async with state.proxy() as date:
        name_year = date['year']
        name_country = date['country']
        name_radius = date['radius']
        name_model = date['model']
        name_model = translit(name_model, language_code='ru', reversed=True)
        name_model = name_model.replace(" ", "_")
        name_full_model = date['full_model']
        name_full_model = name_full_model.replace(" ", "_")
        name_full_model = translit(name_full_model, language_code='ru', reversed=True)
    int_year = int(name_year)
    min_year = str(int_year - 1)
    max_year = str(int_year + 1)
    # /?minyear=1955&maxyear=2022
    # Find_URL = name_country.lower() + name_model.lower() + '/' + name_full_model.lower() + '/?distance=' + name_radius + '&maxyear=' + max_year + '&minyear=' + min_year + '&unsold=1'
    # https://chita.drom.ru/kia/rio/page5/?distance=1000&order=price&unsold=1
    cars_after_find = []
    for i in range(1, 6):
        url = name_country.lower() + name_model.lower() + '/' + name_full_model.lower() + "/page" + str(i) + '/?distance=' + name_radius + '&maxyear=' + max_year + '&minyear=' + min_year + '&unsold=1'
        # print (url)
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        first_find = soup.find('div', class_ ='css-1nvf6xk eojktn00')
        second_find = []
        for first in first_find:
            second_find += first.find_all("a", class_ = "css-xb5nz8 e1huvdhj1")
        # print (find_tegs)
        for items in second_find:
            items = items.get('href')
            href_car.append (items)
        # clear_c_f = [c.text for c in cars_after_find]
        # await message.answer(cars_after_find)
    await message.answer(href_car)
    print(href_car)
    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer ('OK')

# ВЫЗОВ ФИЛЬТРОВ
async def choose_filter(mod):
    if mod == 1:
        filter.first()
    elif mod == 2:
        filter.second()
    else:
        filter.therd()


#РЕГИСТРАТОР   
def register_handlers_find(dp: Dispatcher):
    dp.register_message_handler(Find, commands = ['поиск', 'Поиск', 'Искать', 'искать', 'find'], state = None)
    dp.register_message_handler(model, state = FSMFind.model)
    dp.register_message_handler(full_model, state = FSMFind.full_model)
    dp.register_message_handler(year, state = FSMFind.year)
    dp.register_message_handler(country_find, state = FSMFind.country)
    dp.register_message_handler(radius, state = FSMFind.radius)
    dp.register_message_handler(search_parameter, state = FSMFind.search_parameter)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

async def ckek_model(model, brand):
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM brand WHERE name_brand LIKE ? COLLATE NOCASE", ('%brand%',))
    res_br = cursor.fetchall()
    id_brand = None
    for row in res_br:
        id_brand = row[1]
    cursor.execute("SELECT * FROM model WHERE name_model = ? AND id_model = ?", (model, id_brand))
    results = cursor.fetchall()
    if results == None:
        return True
    else:
        return False

async def check_brand(brand):
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    print (model)
    cursor.execute("SELECT * FROM brand WHERE name_brand LIKE ? COLLATE NOCASE", ('%brand%',))
    # cursor.execute("SELECT * FROM brand WHERE name_brand = ?", (brand,))
    results = cursor.fetchall()
    print (results)
    if results == None:
        return True
    else:
        return False

#ПРОВЕРКА МАРКИ 
def search_json(file_path, word):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for item in data:
        if word.lower() in item.lower():
            return False
    
    return True

async def country(URL_for_find, mess):
    ru_text = mess.lower()
    name_country = ''
    if ru_text.lower() == "москва":
        name_country = "moscow"
    elif (ru_text.lower() == "санкт-петербург") or (ru_text.lower() == "питер"):
        name_country = "spb"
    else:
        name_country = translit(ru_text, language_code='ru', reversed=True)
        name_country = name_country.replace("'", "")
        name_country = name_country.replace(" ", "-")
    ret = ("https://" + name_country + URL_for_find) 
    print (ret)
    return ret

async def checker(URL):
     async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            status_code = response.status
            print(status_code)
            print(URL)
            if status_code == 200:
                return True
            else:
                 return False

		# # https://moscow.drom.ru/kia/all/page2/
		# cars_after_find = []
		# for i in range(1, 6):
		# 	r = main.requests.get("https://" + name_country + URL_for_find + "all/page" + str(i) + "/")
		# 	soup = main.bs(r.text, 'html.parser')
		# 	find_tegs = soup.find_all("div", class_ = "css-l1wt7n e3f4v4l2")
		# 	for items in find_tegs:
		# 		cars_after_find += items.find_all("span")
		# clear_c_f = [c.text for c in cars_after_find]
		# await message.answer(clear_c_f)