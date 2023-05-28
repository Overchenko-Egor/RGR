import first as main
import json
import requests
from transliterate import translit
import os
from data_base import sqlite

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
	Z()
	Y()
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

def Z():
	sqlite.sql_start()
	# with open('all_models_cars.json', 'r', encoding='utf-8') as file:
	# 	data = json.load(file)
	# i = 1
	# for item in data:
	# 	sqlite.sql_add_command(item, i)
	# 	print (i, item)
	# 	i += 1
def Y():
	# https://auto.drom.ru/audi/80/
	URL_main = 'https://auto.drom.ru/'
	with open('all_models_cars.json', 'r', encoding='utf-8') as file:
		data = json.load(file)
	i = 1
	ip_model = 1
	hr = None
	for item in data:
		tmp = []
		name_model = []
		item = translit(item, language_code='ru', reversed=True)
		item = item.replace(" ", "_")
		URL = URL_main + item.lower()
		r = requests.get(URL)
		soup = main.bs(r.text, 'html.parser')
		mc = soup.find_all("a", class_="css-1q66we5 e4ojbx43")
		for hr in mc:
			hr = hr.get('href')
			tmp.append(hr)
		name_model += [c.text for c in mc]
		
		mc2 = soup.find_all("noscript")
		mc3 = []
		for x in mc2:
			mc3 += x.find_all("a", href_ = "")
		for hr in mc3:
			hr = hr.get('href')
			if hr != None:
				tmp.append(hr)
		name_model += [c.text for c in mc3]

		# with open('models/' + item + '.json', 'r', encoding='utf-8') as file:
		# 	data_mod = json.load(file)

		# print(tmp)
		# for num in data_mod:
		# 	sqlite.sql_add_command(j, i, num, hr)
		# print(tmp)
		for num in range(len(name_model)):

			# st1 = tmp[num].split("/")
			# st2 = data_mod[num].replace(" ", "_")
			# st2 = st2.lower()
			# print(st1, "   ", st2)

			

			print(tmp[num], " ----- ", name_model[num])
			href = tmp[num]
			name = name_model[num]
			sqlite.sql_add_command(ip_model, i, name, href)
			ip_model += 1
		i += 1
			

