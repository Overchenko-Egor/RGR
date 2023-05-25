from aiogram import types, Dispatcher
import Filters as filter
import requests
import aiohttp
import json
from transliterate import translit

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

Find_URL = ''

storage = MemoryStorage()
# КЛАСС СОСТОЯНИЙ
class FSMFind(StatesGroup):
    model = State()
    country = State()
    radius = State()
    search_parameter = State()

# Начало
async def Find(message:  types.Message):
	await FSMFind.model.set()
	await message.answer("Введите марку авто")
	
# Модель
async def model(message: types.Message, state: FSMContext):
     mod = message.text
     if search_json('all_models_cars.json', mod):
            await message.answer("Некоректная марка автомобиля. Попробуйте ещё раз!")
            await FSMFind.model.set()
     else:
            async with state.proxy() as date:
                  date ['model'] = message.text
            await FSMFind.next()
            await message.answer("Введите город для подбора авто")

# Город
async def country_find(message:  types.Message, state: FSMContext):
    mod = message.text
    URL_for_find = ".drom.ru/"
    country_name = await country(URL_for_find, mod)
    flag = checker(country_name)

    if (flag):
        async with state.proxy() as date:
            date ['country'] = country_name
            await FSMFind.next()

    else:
         await message.answer("Город указан не корректно. Повторите попытку!")
         await FSMFind.country.set()

    await message.answer("Радиус поиска")    
        
# Радиус
async def radius(message:  types.Message, state: FSMContext):
    async with state.proxy() as date:
        date ['radius'] = message.text
    await FSMFind.next()
    await message.answer("Выберите один из предложенных методов сортировки объявлений\n1 - Цена-пробег\n2 - Количество владельцев\n3 - Наличие ограничений на регистрационные действия")

# Фильтры
async def search_parameter(message:  types.Message, state: FSMContext):
    mod = message.text
    async with state.proxy() as date:
        date ['search_parameter'] = mod
    
    # ЗАВЕРШЕНИЕ
    # async with state.proxy() as date:
    #         await message.answer(str(date))

    # https://barnaul.drom.ru/hyundai/?distance=100
    name_country = None
    name_radius = None
    name_model = None
    async with state.proxy() as date:
        name_country = date['country']
        name_radius = date['radius']
        name_model = date['model']
    Find_URL = name_country + name_model + '/?distance=' + name_radius
    await message.answer(Find_URL)
    await state.finish()



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
    dp.register_message_handler(Find, commands = ['find'], state = None)
    dp.register_message_handler(model, state = FSMFind.model)
    dp.register_message_handler(country_find, state = FSMFind.country)
    dp.register_message_handler(radius, state = FSMFind.radius)
    dp.register_message_handler(search_parameter, state = FSMFind.search_parameter)

# def choose_model():
# 	# @dp.message_handler(content_types = ['text'])
# 	async def Model(message: main.types.Message):
# 		inp_model = message.text.lower()
# 		print ('1')
# 		if inp_model == '':
# 			print ('2')
# 			choose_model()
# 		main.parser_models_cars()
# 		await message.answer(inp_model)

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