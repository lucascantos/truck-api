import boto3
import json
import os
from datetime import datetime

BUCKETNAME = f"{os.environ.get('S3_BUCKET')}-{os.environ.get('STAGE_NAME')}"

def data_lake_name():
    ''' padronização de nomemclatura para o data lake de images e dados '''
    today = datetime.today()
    today_folder = today.strftime('%Y/%m/%d')
    return today_folder

def signed_s3_file(filepath):
    ''' cria uma url com assinatura de acesso temporario para um arquivo do bucket s3 '''
    s3_client = boto3.client('s3')
    response = s3_client.generate_presigned_url('get_object',Params={'Bucket': BUCKETNAME,'Key': filepath}, ExpiresIn=604800)
    return response

def s3_upload(data, filepath):
    ''' Faz upload de arquivo para o buket s3 '''
    # filename = datetime.utcnow().strftime("{}_%Y%m%d".format(product_name))
    # filepath = f"{product_name}/{data_lake_name()}/{filename}.json"

    s3 = boto3.client('s3')
    s3.put_object(Bucket=BUCKETNAME, Key=filepath, Body=json.dumps(data))
    print('File sent to Bucket')
    return (filepath)

def s3_download(filepath):
    s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket=BUCKETNAME, Key=filepath)
    response = json.loads(obj['Body'].read())
    return response

def file_url(filepath):
    return f'https://{BUCKETNAME}.s3.amazonaws.com/{filepath}'

