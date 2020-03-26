import json
from src.helpers.verify import check_param


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def sns_send_inputs(event=None, context=None):
    if check_param(event):
        return check_param(event)    

    report_param = event['queryStringParameters']['report']
    form_inputs = json.loads(event['body'])

    parsed_inputs = list(form_inputs.items())
    response = {
        'statusCode': 200,
        'body': 'Request sent to server'
    }
    sns.send(json.dumps(parsed_inputs), report_param)
    return response

    