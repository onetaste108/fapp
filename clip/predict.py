import torch
import clip
from PIL import Image
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
# device = "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)
print(torch.cuda.get_device_name(0))

with open('index.txt', 'r') as f:
	index = f.read()
index = index.split('\n')

# from google.cloud import storage
# os.environ["GCLOUD_PROJECT"] = "my-project-420-353715"
# bucket_name = 'my-project-420-353715.appspot.com'
# storage_client = storage.Client()

import numpy as np
import time
features = []


from io import BytesIO
import requests
def load_image(url):
	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	return img


start_time = time.time()
index_size = len(index)
BATCH = 100
for i in range(0, index_size, BATCH):
	t = time.time()

	bstart = i
	bend = min(index_size, bstart+BATCH)


	images = []
	for b in range(BATCH):
		url = index[i]
		BUCKET_NAME = 'my-project-420-353715.appspot.com'
		url = 'https://'+BUCKET_NAME+'.storage.googleapis.com/'+url

		image = preprocess(load_image(url)).unsqueeze(0).to(device)
		images.append(image)

	images = torch.cat(images, dim=0)

	with torch.no_grad():
		image_features = model.encode_image(image)
	features.extend(list(image_features.cpu().numpy()))

	speed = (time.time()-start_time)/(i+1)
	remained = (index_size-(i+1))*speed//60
	print(i, "of", index_size, "remaining", remained, "min")

np.save('db_fapello', np.array(features))