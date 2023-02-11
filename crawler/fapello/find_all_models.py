import requests
from bs4 import BeautifulSoup
import os




def get_links(name="top-index", page=1):
	url = f'https://fapello.com/ajax/{name}/page-{page}/'
	# print(url)
	x = requests.get(url)
	if x.status_code == 200:
		soup = BeautifulSoup(x.text, 'html.parser')
		links = [link['href'] for link in soup.find_all('a', href=True)]
		links = [l[len('https://fapello.com/'):] for l in links if l.startswith('https://fapello.com/')]
		links = [l.split('/')[0] for l in links if len(l.split('/')) == 2]
		links = [l for l in links if l not in ['signup', 'signin']]
		links = set(links)
		return links
	else:
		print('Error:', x.status_code)
		return []



import concurrent.futures
def load(pages, BATCH = 32):    
	with concurrent.futures.ThreadPoolExecutor(
		max_workers=BATCH
	) as executor:
		future_to_url = {
			executor.submit(get_links, 'index', page): page
			for page in pages
		}
		results = []
		for future in concurrent.futures.as_completed(
			future_to_url
		):
			url = future_to_url[future]
			try:
				future.result()
				results.append(future.result())
			except Exception as exc:
				results.append(False)
				print(
					"%r generated an exception: %s" % (url, exc)
				)
	return results


with open('models.txt', 'r') as f: models = f.read().split('\n')
models = [m for m in models if len(m)>0]
models = set(models)

# Approx 30000 pages in index

page = 25000
BATCH = 128
while True:
	print(f'Scanning pages {page}-{page+BATCH-1}')
	pages = list(range(page, page+BATCH))
	new_models = load(pages, BATCH)
	new = []
	for m in new_models: new.extend(m)
	if len(new) == 0:
		print('No new models')
		break
	else:
		new = set(new)
		new = new.difference(models)
		print("Found new models:")
		for m in new: print(m)
		with open('models.txt', 'a') as f:
			for m in new:
				f.write('\n'+m)
		models.update(new)
		page += BATCH


