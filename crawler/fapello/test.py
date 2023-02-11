from google.cloud import storage

import os

os.environ["GCLOUD_PROJECT"] = "my-project-420-353715"

storage_client = storage.Client()
bucket = storage_client.bucket('my-project-420-353715.appspot.com',)

def cloud_write(blob_name, file):
    blob = bucket.blob(blob_name)
    with blob.open("wb") as f:
        f.write(file)

import io
def save_image(path, img):
	img_byte_array = io.BytesIO()
	img.save(img_byte_array, format='JPEG')
	cloud_write(path, img_byte_array.getvalue())
