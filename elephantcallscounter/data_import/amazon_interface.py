import os
import boto3
import pandas as pd
from botocore import UNSIGNED
from botocore.config import Config


class AmazonInterface:
    def __init__(self, bucket='congo8khz-pnnn'):
        self.bucket = bucket
        self.s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    def read_from_s3(self):
        objects = []
        paginator = self.s3.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket=self.bucket)
        for page in page_iterator:
            objects.extend(page['Contents'])
        return objects

    def download_s3_file(self, path, filename):
        target_path = f'data/raw/{filename}'
        print(f'Downloading {target_path}...')

        if os.path.exists(target_path):
            print(f'Path {target_path} already exists, skipping.')
        else:
            self.s3.download_file(self.bucket, path, target_path)
            print('Done!')

    def download_all_files(self):
        files = self.read_from_s3()
        filename = ''

        metadata_train_filepath = 'data/metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt'
        metadata_train = pd.read_csv(metadata_train_filepath, sep='\t', header=0)
        train_filenames = metadata_train['filename']

        metadata_test_filepath = 'data/metadata/nn_ele_00-24hr_GeneralTest_v4.txt'
        metadata_test = pd.read_csv(metadata_test_filepath, sep='\t', header=0)
        test_filenames = metadata_test['filename']

        for key in files:
            try:
                path = key['Key']
                filename = path.rsplit('/', 1)[1]
                if filename.endswith('.wav'):
                    if train_filenames.str.contains(filename).any() or test_filenames.str.contains(filename).any():
                        self.download_s3_file(path, filename)
                    else:
                        print(f'Filename {filename} not in train or test set, ignoring.')
            except Exception as e:
                print('Error while downloading ' + filename + ': ' + str(e))
