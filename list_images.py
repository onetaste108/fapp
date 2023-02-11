import os

from google.cloud import storage

os.environ["GCLOUD_PROJECT"] = "my-project-420-353715"
bucket_name = 'my-project-420-353715.appspot.com'

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

images = storage_client.list_blobs(bucket_name, prefix='database/', delimiter='')
# print(len(images))
# images = list(images)
# print(images)
# text = ''
# 	text += '\n'+im.name

i = 0
with open('index.txt', 'w') as f:
	for im in images:
		if im.name[-4:] == '.jpg':
			f.write('\n'+im.name)
			if i % 100 == 0: print(i)
			i += 1
