from google.cloud import storage

import os
os.environ["GCLOUD_PROJECT"] = "my-project-420-353715"


storage_client = storage.Client()
bucket = storage_client.bucket('my-project-420-353715.appspot.com',)

def cloud_write(blob_name, file):
    """Write and read a blob from GCS using file-like IO"""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your new GCS object
    # blob_name = "storage-object-name"

    blob = bucket.blob(blob_name)

    # Mode can be specified as wb/rb for bytes mode.
    # See: https://docs.python.org/3/library/io.html
    with blob.open("wb") as f:
        f.write(file)


from PIL import Image
img = Image.open('test.jpg')
import io





def save_image(path, img):
	img_byte_array = io.BytesIO()
	img.save(img_byte_array, format='JPEG')
	cloud_write(path, img_byte_array.getvalue())
