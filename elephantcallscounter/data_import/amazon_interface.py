import boto3
from botocore import UNSIGNED
from botocore.config import Config


class AmazonInterface:
    def __init__(self, bucket='congo8khz-pnnn'):
        self.bucket = bucket
        self.s3 = boto3.client('s3', config = Config(signature_version = UNSIGNED))

    def read_from_s3(self):
        # download all files and store them in Azure file/blob storage
        files = self.s3.list_objects(Bucket = self.bucket)['Contents']

        return self.s3, files

    def download_s3_file(self, path, filename):
        self.s3.download_file(self.bucket, path, filename)
