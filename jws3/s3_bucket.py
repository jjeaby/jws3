import boto3

bucket_list = []

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    bucket_list.append(bucket.name)

data = open('test.jpg', 'rb')
s3.Bucket('my-bucket').put_object(Key='test.jpg', Body=data)


# S3 Client 생성
s3 = boto3.client('s3')

bucket_name = 'dailywords'
filename = 'requirements.txt'

print(bucket_list)
if bucket_name not in bucket_list:
    s3.create_bucket(Bucket=bucket_name , CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})

s3.upload_file(filename, bucket_name, filename)




# S3에있는 현재 버킷리스트의 정보를 가져온다.
response = s3.list_buckets()

#print(response)

# response에 담겨있는 Buckets의 이름만 가져와 buckets 변수에 배열로 저장.
buckets = [bucket['Name'] for bucket in response['Buckets']]

# S3 버킷 리스트를 출력.
print("Bucket List: %s" % buckets)

