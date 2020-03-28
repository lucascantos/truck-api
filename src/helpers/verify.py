from datetime import datetime
from src.helpers import s3
import json

def check_file(file_url):
    try:
        buffer_data = s3.s3_download(file_url)
    except:
        print('File not found')
        return None
    return buffer_data

def check_param(event, required_params):
    response = None          
    
    if not required_params in event:        
        response = f"{required_params} parameter not found" 
    elif event[required_params] is None:
        response = f"Null parameter: {required_params}" 

    if response:
        return (400, response)
    return response

def check_object(object_id, object_data):
    first_key = list(object_data.keys())[0]
    if object_id > len(object_data[first_key]):
        return make_response(404, 'Not found')
    return

def make_response(code, body):
    response = {
        "statusCode": code,
        "body": json.dumps(body)
    }
    return response
