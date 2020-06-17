import os
from google.cloud import storage

client = storage.Client.from_service_account_json('auth.json')
dir = './artifacts'
bucket = client.get_bucket('aeye-artifacts')

for file in os.listdir('./artifacts'):
    print(f'uploading {file}')
    file_blob = bucket.blob(file)
    with open(os.path.join(dir, file), 'rb') as f:
        file_blob.upload_from_file(f)

