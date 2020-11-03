import requests
from bs4 import BeautifulSoup
from tracks import track_num, cl_track_num
from tabulate import tabulate

session = requests.Session()

base_url = 'https://world-evolved.ru/stats/races'

def search_on_page(url, nickname):

	# url = base_url + '/529?c=S&b=n'

	response = session.get(url)

	page = BeautifulSoup(response.content, 'lxml')

	all_racer_data = page.find_all('div', class_= 'can_open')
	race_name = page.find('div', class_= 'block-title').find('span', id='race-name').text

	def search_on_page(nickname):
		counter = 0
		while counter < len(all_racer_data):
			if all_racer_data[counter].find('a').text == nickname:
				return nickname, counter
			counter += 1

		return False

	def get_all_racer_data(nickname, counter):

		place = all_racer_data[counter].find('div', class_='place').text
		center = all_racer_data[counter].find('div', class_='center').text
		# nickname = all_racer_data[counter].find('a').text
		car = all_racer_data[counter].find('span').text

		subtable = [race_name, place, center, car]

		return subtable

	def racer_data(nickname):
		nickname = nickname.upper().strip()
		if isinstance(search_on_page(nickname), tuple):
			chd_nickname, counter = search_on_page(nickname) # accepting a tuple
			return get_all_racer_data(chd_nickname, counter)
		# return 'Sorry, player is not listed'

	return racer_data(nickname)

table = []

def search_on_server(nickname):
	url = 'https://world-evolved.ru/stats/profiles'
	response = session.get(url + '/' + nickname)
	if response.status_code == 200:
		return True

def get_table_records(nickname, cl, pw):
	print('wait...')
	player_exists = search_on_server(nickname)
	if not player_exists:
		print("Player doesn't exist")
		return False

	global track_num
	track_num = cl_track_num[cl.upper()] + track_num

	x = 0
	while x < len(track_num):
		# for output class tracks
		if x < 6:
			url = base_url + '/' + str(track_num[x])
		else:
			url = base_url + '/' + str(track_num[x]) + '?c={cl}&b={pw}'.format(cl=cl, pw=pw)
		if isinstance(search_on_page(url, nickname), list):
			table.append(search_on_page(url, nickname))

		x += 1

	pw = 'NO' if 'n' else 'YES'

	print('------ ', nickname.upper(), ' --------',cl.upper(),'class ------------------- ', pw,' Power-Ups','---------------')
	print(tabulate(table, headers=['Track', 'rank', 'time', 'car'], tablefmt='psql'))

get_table_records('achilles', 's', 'n')