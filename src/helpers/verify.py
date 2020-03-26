from datetime import datetime
from src.helpers import s3

def check_file(report_param):
    today_date = datetime.utcnow().strftime('%Y%m%d')
    file_url = f'{report_param}/{s3.data_lake_name()}/{report_param}_{today_date}.json'
    try:
        buffer_data = s3.s3_download(file_url)
    except:
        return None
    return buffer_data

def check_param(event):
    response = None
    if not event['queryStringParameters']:
        response = "No query parameters given"

    if not 'report' in event['queryStringParameters']:
        response = "'report' parameter not found"

    if response:
        return response