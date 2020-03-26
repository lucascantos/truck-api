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
    if not required_params in event:
        response = f"{required_params} parameter not found"

    if response:
        return (400, response)

