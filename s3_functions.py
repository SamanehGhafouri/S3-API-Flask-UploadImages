import boto3
import uuid
import os


def upload_file_obj(file, bucket, file_name):
    """
    Function to upload a file to an S3 bucket without saving it locally
    """
    s3 = boto3.client('s3')
    s3.upload_fileobj(file, bucket, file_name)


def download_file(file_name, bucket):
    """
    Function to downloads a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents


def create_random_id(filename):
    """
    Randomly generated key for file
    """
    file_ext = os.path.splitext(filename)[1]
    return ''.join([str(uuid.uuid4()), file_ext])