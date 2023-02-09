import requests
from bs4 import BeautifulSoup
import os




def get_links(name="top-followers", page=1):
	url = f'https://fapello.com/ajax/{name}/page-{page}/'
	print(url)
	x = requests.get(url)
	if x.status_code == 200:
		soup = BeautifulSoup(x.text, 'html.parser')
		links = [link['href'] for link in soup.find_all('a', href=True)]
		if len(links) > 0:
			os.makedirs(name, exist_ok=True)
			with open(f'{name}/page-{page}.txt', 'w') as f:
				txt = '\n'.join(links)+'\n'
				print(txt)
				f.write(txt)
			return links
		else:
			raise Exception("No links found")
	raise Exception(x)


page = 1
while True:
	try:
		get_links(page = page)
		page += 1
	except Exception as err:
		print(err)

