from datetime import datetime
from src.helpers import s3

def check_file(file_url):
    try:
        buffer_data = s3.s3_download(file_url)
    except:
        print('Error')
        return None
    return buffer_data

def check_param(event, required_params):
    response = None
    if not event['queryStringParameters']:
        response = "No query parameters given"

    for param in required_params:            
        if not param in event['queryStringParameters']:
            response = f"{param} parameter not found"

    if response:
        return (400, response)

