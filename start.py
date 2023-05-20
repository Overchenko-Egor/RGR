import first as main

def start():
    parser_models_cars()
    # await message.answer(parser_models_cars())
        

def parser_models_cars():
	r = main.requests.get(main.URL_main)
	soup = main.bs(r.text, 'html.parser')
	mc = soup.find_all("a", class_="css-1q66we5 e4ojbx43")
	other_models = soup.find_all("noscript")
	for items in other_models:
		mc += items.find_all("a", href_ = "")
	clear_m_c = [c.text for c in mc]
	Write_json(clear_m_c)

def Write_json(clear_m_c):
	with open('all_models_cars.json', 'w', encoding="utf-8") as outfile:
 		main.json.dump(clear_m_c, outfile, ensure_ascii=False)