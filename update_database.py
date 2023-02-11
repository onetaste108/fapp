from google.cloud import firestore
import os

os.environ["GCLOUD_PROJECT"] = "my-project-420-353715"
db = firestore.Client()


with open('index.txt', "r") as f:
	index = f.read()

index = index.split('\n')


# START = 100000
# index = index[START:]



data = []
for i in range(len(index)):
# for i in range(1):
	url = index[i]
	name = url.split('/')[-1].split('_')[0]
	field = {
		"index": i,
		"url": index[i],
		"model": name
	}
	data.append(field)
	if i % 1000 == 0:
		print(i, 'of', len(index))




# print(data)
print(len(data))

count = 0
batch = db.batch()
for i in range(len(data)):
	count += 1
	# db.collection('images').document(str(i)).set(data[i])
	img_ref = db.collection('images').document(str(i))
	batch.set(img_ref, data[i])
	if count == 500 or i == len(data)-1:
		batch.commit()
		print("Committed", i)
		count = 0
		batch = db.batch()








# # Commit the batch
