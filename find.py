import first as main

def find():
	@main.dp.message_handler(content_types = ['text'])
	async def Find(message:  main.types.Message):
		await message.answer("Введите марку авто")
		choose_model()
		await message.answer("Введите населенный пункт")
		URL_for_find = ".drom.ru/auto/"
		country(URL_for_find)
    
def choose_model():
	# @dp.message_handler(content_types = ['text'])
	async def Model(message: main.types.Message):
		inp_model = message.text.lower()
		print ('1')
		if inp_model == '':
			print ('2')
			choose_model()
		main.parser_models_cars()
		await message.answer(inp_model)
		

def country(URL_for_find):
	@main.dp.message_handler(content_types = ['text'])
	async def Country(message: main.types.Message):
		ru_text = message.text.lower()
		if message.text.lower() == "москва":
			name_country = "moscow"
		elif (message.text.lower() == "санкт-петербург") or (message.text.lower() == "питер"):
			name_country = "spb"
		else:
			name_country = main.translit(ru_text, language_code='ru', reversed=True)
			name_country = name_country.replace("'", "")
			name_country = name_country.replace(" ", "-")
		await message.answer(name_country)
		await message.answer("Ваш запрос обрабатывается...")

		# https://moscow.drom.ru/kia/all/page2/
		cars_after_find = []
		print(cars_after_find)
		for i in range(1, 6):
			r = main.requests.get("https://" + name_country + URL_for_find + "all/page" + str(i) + "/")
			soup = main.bs(r.text, 'html.parser')
			find_tegs = soup.find_all("div", class_ = "css-l1wt7n e3f4v4l2")
			for items in find_tegs:
				cars_after_find += items.find_all("span")
		clear_c_f = [c.text for c in cars_after_find]
		await message.answer(clear_c_f)