import os
from boto3.session import Session
import boto3
import botocore
import pandas as pd
from IPython.display import display, Markdown
from botocore.client import Config
from botocore import UNSIGNED
# Loading the training file info
training_files = pd.read_csv('data/nn_ele_hb_00-24hr_TrainingSet_v2.txt',delimiter="\t")
training_files.head()
file_list = training_files['filename'].unique()
len(file_list)
# Loading these files from S3
s3 = boto3.resource(
    's3',
    aws_access_key_id='',
    aws_secret_access_key='',
    config=Config(signature_version=UNSIGNED)
)
BUCKET = 'congo8khz-pnnn'
my_bucket = s3.Bucket(BUCKET)
file_list[1]
print(my_bucket.objects.all())

for file in file_list:  # + bottomFiles:
    my_bucket.download_file(file, file)

contents = [_.key for _ in my_bucket.objects.all()]
print(contents)
