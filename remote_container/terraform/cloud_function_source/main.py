import base64
import functions_framework
import qrcode
from io import BytesIO
import os
import json
from google.cloud import storage

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def entry_point(cloud_event):
    data = base64.b64decode(cloud_event.data["message"]["data"])
    data_loaded = json.loads(data)
    url = data_loaded['url']
    room_id = data_loaded['room_id']

    if str(url)=="del":
        delete_img_from_storage(room_id)
    else: 
        img = generate_qrcode(url)
        save_img_to_storage(img, room_id)

def generate_qrcode(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=40,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img

def save_img_to_storage(img, room_id):
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ.get("BUCKET_NAME"))
    blob = bucket.blob(f"{room_id}.png")

    img_buffer.seek(0)
    blob.upload_from_file(img_buffer, content_type='image/png')

def delete_img_from_storage(room_id):
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ.get("BUCKET_NAME"))
    blob = bucket.blob(f"{room_id}.png")
    blob.delete()
