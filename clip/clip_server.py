import torch
import clip
from PIL import Image

# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)

import os
import numpy as np

features_dir = '../weights'
fps = os.listdir(features_dir)
indices = [int(f.split('.')[0]) for f in fps]
indices.sort()

all_size = 0
features = []
for idx in indices:
	arr = np.load(features_dir+'/'+f'{idx}.npy')[0]
	arr = np.float32(arr)
	all_size += arr.shape[0]
	features.append(arr)
	if idx == 0:
		features.append(np.ones_like(arr)*10.0)

print('all size', all_size)
print('supposed', indices[-1]+1024)

for f in features:
	assert f.shape[1] == 768, f.shape
features = np.concatenate(features, 0)

fap_features = features
fap_features_ = torch.from_numpy(fap_features).to(device)
fap_features = fap_features_
fap_features /= fap_features.norm(dim=-1, keepdim=True)

def find_best_feature(image_features, fap_features, size=10):
	image_features /= image_features.norm(dim=-1, keepdim=True)
	similarity = (100.0 * image_features @ fap_features.T).softmax(dim=-1)
	values, best = similarity[0].topk(size)
	print("VB", values, best)
	values = values.cpu().numpy()
	best = best.cpu().numpy()
	return values, best

def sim_image(image, fap_features, size=10):
	image = preprocess(image).unsqueeze(0).to(device)
	with torch.no_grad():
		image_features = model.encode_image(image)
	return find_best_feature(image_features, fap_features, size)

def sim_text(text, fap_features, size=10):
	text = clip.tokenize([text]).to(device)
	with torch.no_grad():
		image_features = model.encode_text(text)
	print('finding text..')
	return find_best_feature(image_features, fap_features, size)

def sim_db(id, fap_features, size=10):
	feat = fap_features[id:id+1]
	return find_best_feature(feat, fap_features, size)




with open('../index.txt', 'r') as f:
	index = f.read().split('\n')

from io import BytesIO
import requests
def load_image(url):
	try:
		response = requests.get(url)
		# assert url[-4:] == '.jpg', url
		img = Image.open(BytesIO(response.content))
		return img
	except Exception as err:
		print(err)
		return None

def load_index(idx):
	url = index[idx]
	print('loading', url)
	url = 'https://my-project-420-353715.appspot.com.storage.googleapis.com/'+url
	img = load_image(url)
	return img


from google.cloud import firestore
import os

print("Connecting..")

os.environ["GCLOUD_PROJECT"] = "my-project-420-353715"
db = firestore.Client()

import threading
# Create an Event for notifying main thread.
callback_done = threading.Event()




def process_request(value, key):
	SIZE = 100
	if key == "prompt":
		assert type(value) == str
		print('TEXT', value)
		value, best = sim_text(value, fap_features, SIZE)
		print('text done')
	elif key == "url":
		print('IMAGE', value)
		image = load_image(value)
		if image is None:
			print('Error 1', value)
			return None
		value, best = sim_image(image, fap_features, SIZE)
	elif key == "index":
		print('INDEX', value)
		if value >= len(fap_features) or (value >= 1024 and value < 1024*2):
			image = load_index(value)
			if image is None:
				print('Error 1', value)
				return None
			value, best = sim_image(image, fap_features, SIZE)
		else:
			value, best = sim_db(value, fap_features, SIZE)
	else:
		print("ERROR", key)
		return []

	

	outs = []
	for b in best:
		outs.append(int(b))
	print(outs)
	print('returning')
	return outs







# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
	print('NEW')
	for doc in doc_snapshot:
		data = doc.to_dict()
		value = data['id']
		print(data)
		print("Update id:", value)


		prompt = db.collection(u'prompts').document(value).get().to_dict()
		keys = list(prompt.keys())
		key = keys[0]
		prompt = prompt[key]

		print("Prompt:", prompt)

		# DO SOMETHING
	
		best = process_request(prompt, key)
		print('returned', best)
		if best is not None:
		# 

			resp_ref = db.collection('clip_server').document('response')
			resp_ref.update({
				value: best
			})
			print('uploaded')
		else:
			print("Else is none")
		print("Done, waiting...")

	callback_done.set()

doc_ref = db.collection(u'clip_server').document(u'request')

# doc = doc_ref.get()
# if doc.exists:
#     print(f'Document data: {doc.to_dict()}')
# else:
#     print(u'No such document!')

# Watch the document
print("Listening..")
doc_watch = doc_ref.on_snapshot(on_snapshot)


import time
while True:
	time.sleep(1)
