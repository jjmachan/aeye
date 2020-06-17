import os
from google.cloud import storage

client = storage.Client.from_service_account_json('auth.json')
dir = './artifacts_test'
bucket = client.get_bucket('aeye-artifacts')

for blob in bucket.list_blobs():
    print('downloading: ',blob.name)
    with open(os.path.join(dir, blob.name), 'wb') as f:
        blob.download_to_file(f)
