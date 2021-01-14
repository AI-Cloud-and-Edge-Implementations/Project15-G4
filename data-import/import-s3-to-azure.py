import os

import boto3
from botocore import UNSIGNED
from botocore.config import Config
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

try:
    print("Azure Blob storage v" + __version__)
except Exception as ex:
    print('Exception:')
    print(ex)

# create a container (replace account key with actual one)
blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=project15storage;AccountKey=XXX;EndpointSuffix=core.windows.net')
container_name = 'elephant'
container_client = blob_service_client.create_container(container_name)

# download all files and store them in Azure file/blob storage
files=s3.list_objects(Bucket='congo8khz-pnnn')['Contents']
for key in files:
    try:
        path = key['Key']
        filename = path.rsplit('/', 1)[1]
        if filename.endswith('.wav'):
            print('Downloading ' + path + '...')
            s3.download_file('congo8khz-pnnn', path, filename)
            # store in blob
            print('Storing ' + filename + ' in Azure Blob...')
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
            with open(filename, "rb") as data:
                blob_client.upload_blob(data)
            # delete local file
            os.remove(filename)
            print('Done!')
    except Exception as e:
        print('Error while downloading ' + filename + ': ' + str(e))

