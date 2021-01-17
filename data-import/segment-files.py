import os
import pandas as pd
from pydub import AudioSegment
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.identity import DefaultAzureCredential
from azureml.core.authentication import MsiAuthentication

try:
    print("Azure Blob storage v" + __version__)
except Exception as ex:
    print('Exception:')
    print(ex)

blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=project15;AccountKey=XXX;EndpointSuffix=core.windows.net')

container_name = 'elephant-sound-data'

blob_container_client = blob_service_client.get_container_client(container_name)

# read metadata
metadata_filepath = 'metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt'
metadata = pd.read_csv(metadata_filepath, sep='\t', lineterminator='\r', header=0)
print(f'Using metadata file {metadata_filepath}')

# process raw files
#for filename in os.listdir('data'):
for blob in blob_container_client.list_blobs():
    filename = blob.name
    print(f'Processing {filename}...')

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    # download file
    download_path = 'data/' + filename
    with open(download_path, 'wb') as download_file:
        dir = download_path.split('/')[-1]
        if (not os.path.exists(dir)):
            print(f' Creating directory {dir}...')
            os.mkdir(dir)

        print(f' Downloading {download_path}...')
        download_file.write(blob_client.download_blob().readall())

    file = AudioSegment.from_wav(download_path)

    print(f'Processing blob {x}...')

    # get the relevant segments from the metadata
    metadata_segments = metadata[metadata['filename'] == filename]

    for index, metadata_segment in metadata_segments.iterrows():
        try:
            selection = metadata_segment["Selection"].lstrip()
            print(f' Generating segment {selection}...')

            start = metadata_segment['File Offset (s)']  # ms
            duration = metadata_segment['duration'] * 1000  # ms
            end = start + duration

            segment = file[start:end]

            marginal = str(metadata_segment['marginals']).strip()
            segment_path = f'segments/{filename}_segment_{selection}_{marginal}.wav'
            segment.export(segment_path, format='wav')
            print(f' Found segment of {segment.duration_seconds} seconds, exported to {segment_path}.')
        except Exception as e:
            print('  Error when creating segment: ' + str(e))

    # remove local file
    os.remove(download_path)

    print('Done')
