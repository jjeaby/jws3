import logging

import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def delete_bucket(bucket_name):
    try:
        s3_client = boto3.client('s3')
        s3_client.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_bucket():
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    bucket_list = []
    # Output the bucket names
    for bucket in response['Buckets']:
        bucket_list.append(bucket["Name"])

    return bucket_list


def upload_file(file_name, bucket, object_name=None, acl=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False


    [Example]
    s3 = boto3.client('s3')
    with open("FILE_NAME", "rb") as f:
        s3.upload_fileobj(f, "BUCKET_NAME", "OBJECT_NAME")
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        if acl == 'public':
            acl_option = {'ACL': 'public-read'}
            response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=acl_option)
        else:
            response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_files(bucket_name):
    try:
        s3_client = boto3.client('s3')
        files_list = s3_client.list_objects(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return []
    return files_list


def get_all_s3_keys(bucket):
    """Get a list of all keys in an S3 bucket."""
    keys = []
    s3_client = boto3.client('s3')

    kwargs = {
        'Bucket': bucket
    }

    while True:
        resp = s3_client.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            keys.append(obj['Key'])

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break

    return keys


def get_pages_s3_keys(bucket, NextContinuationToken=None, search=None, limit=10):
    """Get a list of all keys in an S3 bucket."""
    keys = {}
    keys["keys"] = []

    s3_client = boto3.client('s3')

    kwargs = {
        'Bucket': bucket,
        'MaxKeys': 1,
    }

    if NextContinuationToken != None:
        kwargs['ContinuationToken'] = NextContinuationToken

    # if search != None:
    #     kwargs['Prefix'] = str(search)

    limit_counter = 0
    counter = 0

    while limit_counter < limit:
        resp = s3_client.list_objects_v2(**kwargs)

        if resp != None and 'Contents' in resp:
            for obj in resp['Contents']:

                if 'NextContinuationToken' in resp:
                    keys['NextContinuationToken'] = resp['NextContinuationToken']
                    kwargs['ContinuationToken'] = resp['NextContinuationToken']
                    if str(obj['Key']).find(search) >= 0:
                        keys["keys"].append(obj)
                        limit_counter = limit_counter + 1


                else:
                    keys['NextContinuationToken'] = ''
                    kwargs['ContinuationToken'] = ''
                    if str(obj['Key']).find(search) >= 0:
                        keys["keys"].append(obj)
                        limit_counter = limit_counter + 1

                    break


    return keys


if __name__ == '__main__':
    # ret = delete_bucket('dailywords')
    # print("delete_bucket:", ret)
    ret = create_bucket('dailywords', 'ap-northeast-2')
    print("create_bucket:", ret)
    print("-"*100)

    ret = upload_file('/home/jjeaby/Dev/02.jjeaby.github/jws3/jws3/util.py', 'dailywords', 'util.py', acl='public')
    print("upload_file:", ret)
    print("-"*100)

    ret = upload_file('/home/jjeaby/Dev/02.jjeaby.github/jws3/jws3/util.py', 'dailywords', 'util2.py', acl='public')
    print("upload_file:", ret)
    print("-"*100)

    ret = list_files('dailywords')
    print('list_files', ret)
    print("-"*100)

    ret = get_pages_s3_keys('dailywords', limit=1, search='util')
    print('get_pages_s3_keys_limit=1', ret)
    print("-"*100)

    ret = get_pages_s3_keys('dailywords', limit=2, search='util')
    print('get_pages_s3_keys', ret)
