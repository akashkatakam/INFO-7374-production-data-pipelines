import boto3
import requests


def upload_file_tos3(file_name, bucket, body):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3', region_name='us-east-1')
    response1 = s3_client.put_object(Body=body,
                                     Bucket=bucket,
                                     Key=file_name)

    return response1

def grant_public_access(bucket,key):
    s3 = boto3.resource('s3')
    object_acl = s3.ObjectAcl(bucket,key)
    response = object_acl.put(ACL='public-read')

def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
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
    print(contents)
    return contents