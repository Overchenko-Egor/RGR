from aiogram import types, Dispatcher
import Filters as filter
import requests
from data_base import sqlite
import aiohttp
import json
from transliterate import translit

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
    mod = mod.replace(" ", "_")
    if search_json('all_models_cars.json', mod):
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
    brand = ''
    async with state.proxy() as date:
        brand = date['model']
    tmp = 'models/' + brand + '.json'
    print (tmp)
    if search_json(tmp, mod):
        await message.answer("Некоректная модель автомобиля. Попробуйте ещё раз!")
        await FSMFind.full_model.set()
    else:
        async with state.proxy() as date:
            date ['full_model'] = message.text
        await FSMFind.next()
        await message.answer("Введите город для подбора авто")

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
    
    # ЗАВЕРШЕНИЕ
    name_country = None
    name_radius = None
    name_model = None
    name_full_model = None
    async with state.proxy() as date:
        name_country = date['country']
        name_radius = date['radius']
        name_model = date['model']
        name_model = translit(name_model, language_code='ru', reversed=True)
        name_model = name_model.replace(" ", "_")
        name_full_model = date['full_model']
        name_full_model = name_full_model.replace(" ", "_")
        name_full_model = translit(name_full_model, language_code='ru', reversed=True)
    Find_URL = name_country.lower() + name_model.lower() + '/' + name_full_model.lower() + '/?distance=' + name_radius
    await message.answer(Find_URL)
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
     

#ПРОВЕРКА МАРКИ 
def search_json(file_path, word):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for item in data:
        if word.lower() in item.lower():
            return False
    
    return True


#РЕГИСТРАТОР   
def register_handlers_find(dp: Dispatcher):
    dp.register_message_handler(Find, commands = ['поиск', 'Поиск', 'Искать', 'искать'], state = None)
    dp.register_message_handler(model, state = FSMFind.model)
    dp.register_message_handler(full_model, state = FSMFind.full_model)
    dp.register_message_handler(country_find, state = FSMFind.country)
    dp.register_message_handler(radius, state = FSMFind.radius)
    dp.register_message_handler(search_parameter, state = FSMFind.search_parameter)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

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