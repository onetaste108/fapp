import os
import requests
import shutil

from google.cloud import storage

os.environ["GCLOUD_PROJECT"] = "my-project-420-353715"
bucket_name = 'my-project-420-353715.appspot.com'

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

def cloud_write(blob_name, file):
    blob = bucket.blob(blob_name)
    with blob.open("wb") as f:
        f.write(file)

import io
def save_image(path, file):
	# img_byte_array = io.BytesIO()
	# img.save(img_byte_array, format='JPEG')
	cloud_write(path, file)





with open("top-followers.txt", "r") as f:
	girls = f.read()

girls = girls.split('\n')
names = []
for g in girls:
	name = g[len('https://fapello.com/'):-1]
	names.append(name)
# print(names[:10])
n = names[0]



import concurrent.futures

def get_link(n, id, ext):
	index = "0000"[:-len(str(id))]+str(id)
	fn = f"{n}_{index}.jpg"
	link = f"https://fapello.com/content/{n[0]}/{n[1]}/{n}/{int(index[0])+1}000/{n}_{index}.{ext}"
	return link

def save_image_from_url(name, index, output_folder):

	urls = [get_link(name, index, ext) for ext in ['jpg', 'mp4', 'm4v', 'jpeg', 'png']]
	for url in urls:
		x = requests.get(url, stream=True)
		if x.status_code == 200:
			output_path = os.path.join(
				output_folder, url.split('/')[-1]
			)
			save_image(output_path, x.content)
			print("Saved:", url)
			return True
	print("Error getting data for {name} : {index}")
	return False

def load(name, indices, output_folder, BATCH = 10):    
	with concurrent.futures.ThreadPoolExecutor(
		max_workers=BATCH
	) as executor:
		future_to_url = {
			executor.submit(save_image_from_url, name, index, output_folder): index
			for index in indices
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






from bs4 import BeautifulSoup
def get_links(name):
	indices = []
	id = 1
	all_indices = []
	while True:
		url = f"https://fapello.com/ajax/model/{name}/page-{id}/"
		print("Scanning", url)
		x = requests.get(url)
		if x.status_code == 200:
			soup = BeautifulSoup(x.text, 'html.parser')
			links = soup.find_all("a")
			links = [l['href'] for l in links if name in l['href']]
			indices = []
			for l in links:
				try:
					ind = int(l.split('/')[-2])
					indices.append(ind)
				except Exception as err:
					print(err)
			id += 1
			all_indices.extend(indices)
			print(' '.join([str(i) for i in indices]))
			if len(indices) == 0: break
		else:
			print("Error status", x.status_code)
			break
		
	return all_indices


def parse_model(name):
	models_dir = 'database/fapello/models/'
	dir = models_dir+name+"/"

	with open('logs.txt', 'r') as f:
		logs = f.read()
	models = logs.split('\n')

	if name in models:
		f"Model {name} already downloaded"
		return
	idc = get_links(name)
	# os.makedirs(dir, exist_ok=True)
	existed = storage_client.list_blobs(bucket_name, prefix=dir, delimiter='/')
	existed = [f.name.split('/')[-1].split('.')[0] for f in existed]
	existed = [f[len(f'{name}_'):] for f in existed]
	existed = [int(f) for f in existed]
	existed = set(existed)
	idc = [i for i in idc if i not in existed]
	BATCH = 50
	batch_id = 0
	while BATCH*batch_id < len(idc):
		batch_start = batch_id*BATCH
		batch_end = batch_start+BATCH
		# print(batch_id, batch_start, batch_end, len(idc))
		batch_end = min(batch_end, len(idc))
		indices = idc[batch_start:batch_end]
		print("Parsing", name, " ".join([str(i) for i in indices]))
		results = load(name, indices, dir, BATCH=BATCH)
		batch_id += 1

	with open('logs.txt', 'a') as f:
		f.write('\n'+name)
	# os.rename(dir, dir[:-2]+'/')
	# bucket.blob(dir).rename(dir[:-2]+'/')




# parse_model("catkitty21")
# parse_model("adriana-chechik")



for name in names:
	parse_model(name)


