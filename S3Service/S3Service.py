import boto3
from botocore.exceptions import NoCredentialsError, ClientError

class S3Service:
    def __init__(self, bucket_name, aws_access_key_id=None, aws_secret_access_key=None, region_name='us-west-2'):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def upload_file(self, file_name, object_name=None):
        """Upload a file to the S3 bucket."""
        if object_name is None:
            object_name = file_name
        try:
            self.s3_client.upload_file(file_name, self.bucket_name, object_name)
            print(f"File '{file_name}' uploaded to '{self.bucket_name}/{object_name}'.")
        except FileNotFoundError:
            print(f"The file '{file_name}' was not found.")
        except NoCredentialsError:
            print("Credentials not available.")
        except ClientError as e:
            print(f"An error occurred: {e}")

    def create_folder(self, folder_name):
        """Create a folder in the S3 bucket."""
        if not folder_name.endswith('/'):
            folder_name += '/'
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=folder_name)
            print(f"Folder '{folder_name}' created in bucket '{self.bucket_name}'.")
        except ClientError as e:
            print(f"An error occurred: {e}")

    def delete_file(self, object_name):
        """Delete a file from the S3 bucket."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            print(f"File '{object_name}' deleted from bucket '{self.bucket_name}'.")
        except ClientError as e:
            print(f"An error occurred: {e}")

    def delete_folder(self, folder_name):
        """Delete a folder and its contents from the S3 bucket."""
        if not folder_name.endswith('/'):
            folder_name += '/'
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=folder_name)
            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        self.s3_client.delete_object(Bucket=self.bucket_name, Key=obj['Key'])
                        print(f"Deleted '{obj['Key']}' from bucket '{self.bucket_name}'.")
            print(f"Folder '{folder_name}' and all its contents have been deleted.")
        except ClientError as e:
            print(f"An error occurred: {e}")
