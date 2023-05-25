import first as main
import json
import requests
from transliterate import translit
import os

def start():
    parser_models_cars()
    # await message.answer(parser_models_cars())
        

def parser_models_cars():
	r = requests.get(main.URL_main)
	soup = main.bs(r.text, 'html.parser')
	mc = soup.find_all("a", class_="css-1q66we5 e4ojbx43")
	other_models = soup.find_all("noscript")
	for items in other_models:
		mc += items.find_all("a", href_ = "")
	clear_m_c = [c.text for c in mc]
	name_file = 'all_models_cars.json'
	# Write_json(clear_m_c, name_file)
	y()
	# parser_full_models_cars()
        
def parser_full_models_cars():
	with open('all_models_cars.json', 'r', encoding='utf-8') as file:
		data = json.load(file)
	for item in data:
		name = item
		print (name)
		URL = 'https://auto.drom.ru/' + name.lower() + '/'
		r = requests.get(URL)
		soup = main.bs(r.text, 'html.parser')
		mc = soup.find_all("a", class_="css-1q66we5 e4ojbx43")
		other_models = soup.find_all("noscript")
		for items in other_models:
			mc += items.find_all("a", href_ = "")
		clear_m_c = [c.text for c in mc]
		print(clear_m_c)
		name_file = 'models/' + name + '.json'
		Write_json(clear_m_c, name_file)
		
def x():
	with open('all_models_cars.json', 'r', encoding='utf-8') as file:
		data = json.load(file)
	for item in data:
		name = item
		# Audi.json
		string = 'models/' + name + '.json'
		with open(string, 'r', encoding='utf-8') as file:
			js = json.load(file)
		if len(js) == 0:
			print(name)
			tmp = name
			tmp = translit(tmp, language_code='ru', reversed=True)
			tmp = tmp.replace(" ", "")
			if tmp == 'SsangYong':
				tmp = 'Ssang_Yong'
			
			if tmp == 'EXEED':
				tmp = 'cheryexeed'
			print(tmp)
			URL = 'https://auto.drom.ru/' + tmp.lower() + '/'
			r = requests.get(URL)
			soup = main.bs(r.text, 'html.parser')
			mc = soup.find_all("a", class_="css-1q66we5 e4ojbx43")
			# other_models = soup.find_all("noscript")
			# for items in other_models:
			# 	mc += items.find_all("a", href_ = "")
			clear_m_c = [c.text for c in mc]
			print(clear_m_c)
			name_file = 'models/' + name + '.json'
			Write_json(clear_m_c, name_file)

def y():
	files = os.listdir('models')

	# Переименование файлов
	for filename in files:
		new_filename = filename.lower()
		os.rename(os.path.join('models', filename), os.path.join('models', new_filename))

def Write_json(clear_m_c, name_file):
	with open(name_file, 'w', encoding="utf-8") as outfile:
 		json.dump(clear_m_c, outfile, ensure_ascii=False)



def search_json(file_path, word):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for item in data:
        if word.lower() in item.lower():
            return False
    return True