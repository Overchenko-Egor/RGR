import first as main
from first import dp, types, Dispatcher
import json

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()
class FSMFind(StatesGroup):
    model = State()
    country = State()
    radius = State()
    search_parameter = State()

# @dp.message_handler(commands='find', state = None)
async def Find(message:  types.Message):
	await FSMFind.model.set()
	await message.answer("Введите марку авто")
	

# @dp.message_handler(commands='model', state = FSMFind.model)
async def model(message:  types.Message, state: FSMContext):
	mod = message.text
	if search_json('all_models_cars.json', mod):
		await FSMFind.model.set()
		await message.answer("Некоректная марка автомобиля. Попробуйте ещё раз!")
	else:
		async with state.proxy() as date:
			date['model'] = message.model[0].file_id
		await FSMFind.next()
		await message.answer("Введите город для подбора авто")
                

@dp.message_handler(commands='country', state = FSMFind.country)
async def country(message:  types.Message):
	await FSMFind.model.set()
	await message.answer("Введите марку авто")
def search_json(json_file, search_key):
    with open(json_file) as file:
        data = json.load(file)
    results = []
    search_recursive(data, search_key.lower(), results)  # Преобразуем ключ к нижнему регистру
    if len(results) == 0:
         return False
    else:
         return True

def search_recursive(data, search_key, results):
    if isinstance(data, dict):
        for key, value in data.items():
            if key.lower() == search_key:  # Сравниваем ключи без учета регистра
                results.append(value)
            else:
                search_recursive(value, search_key, results)
    elif isinstance(data, list):
        for item in data:
            search_recursive(item, search_key, results)
            
def register_handler(dp: Dispatcher):
	dp.register_message_handler(Find, commands = ['find'], state = None)
	dp.register_message_handler(model, state = FSMFind.model)

# def find():
# 	print('1')
# 	async def handle_message(message: main.types.Message):
# 		await message.answer("Введите марку авто")
# 		choose_model()
# 		await message.answer("Введите населенный пункт")
# 		URL_for_find = ".drom.ru/auto/"
# 		country(URL_for_find)
    
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
		

# def country(URL_for_find):
# 	@main.dp.message_handler(content_types = ['text'])
# 	async def Country(message: main.types.Message):
# 		ru_text = message.text.lower()
# 		if message.text.lower() == "москва":
# 			name_country = "moscow"
# 		elif (message.text.lower() == "санкт-петербург") or (message.text.lower() == "питер"):
# 			name_country = "spb"
# 		else:
# 			name_country = main.translit(ru_text, language_code='ru', reversed=True)
# 			name_country = name_country.replace("'", "")
# 			name_country = name_country.replace(" ", "-")
# 		await message.answer(name_country)
# 		await message.answer("Ваш запрос обрабатывается...")

# 		# https://moscow.drom.ru/kia/all/page2/
# 		cars_after_find = []
# 		print(cars_after_find)
# 		for i in range(1, 6):
# 			r = main.requests.get("https://" + name_country + URL_for_find + "all/page" + str(i) + "/")
# 			soup = main.bs(r.text, 'html.parser')
# 			find_tegs = soup.find_all("div", class_ = "css-l1wt7n e3f4v4l2")
# 			for items in find_tegs:
# 				cars_after_find += items.find_all("span")
# 		clear_c_f = [c.text for c in cars_after_find]
# 		await message.answer(clear_c_f)