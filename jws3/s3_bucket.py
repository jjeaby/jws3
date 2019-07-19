import boto3


https://github.com/join?source=header-home


# S3 Client 생성
s3 = boto3.client('s3')

bucket_name = 'dailywords'
filename = 'requirements.txt'


#s3.create_bucket(Bucket=bucket_name , CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})

s3.upload_file(filename, bucket_name, filename)



# S3에있는 현재 버킷리스트의 정보를 가져온다.
response = s3.list_buckets()

#print(response)

# response에 담겨있는 Buckets의 이름만 가져와 buckets 변수에 배열로 저장.
buckets = [bucket['Name'] for bucket in response['Buckets']]

# S3 버킷 리스트를 출력.
print("Bucket List: %s" % buckets)

