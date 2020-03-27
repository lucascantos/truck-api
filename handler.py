import json
import pandas as pd
from src.user_objects import user_list
from src.helpers.verify import check_param
from src.helpers import s3

def get_users(event=None, context=None):
    '''
    Get filter parameters
    load users on pandas
    check filters with headers (continue)
    filter data
    return json of data
    200
    '''
    users_db = user_list()
    body = users_db.users_data
    if check_param(event, 'queryStringParameters'):
        filter_params = event['queryStringParameters']
        body = users_db.filter_users(filter_params)
    make_response(200, body)


def add_user(event=None, context=None):
    '''
    Check if parameters are right [name, age, gender, ownAuto, licence, vehicleType] 400
    Load users on pandas
    Include data do table
    Save users back to s3
    201
    '''
    user_params = ['name', 'age', 'gender', 'ownAuto', 'licence', 'vehicleType']

    if error := check_param(event, 'body'):
        return make_response(error[0], error[1])  

    for param in user_params:        
        if error := check_param(event['body'], param):
            return make_response(error[0], error[1])  
          
    new_user_params = json.loads(event['body'])
    new_user_params['status'] = 0

    users_db = user_list()
    users_db.add_user(new_user_params)
    users_db.save_users()

    return make_response(201, f'New user added: {new_user_params["name"]}')


def get_user_info(event=None, context=None):
    '''
    load users on pandas
    check if user exists 404
    get user data
    return json of data
    200
    '''
    if error := check_param(event['path'], 'id'):
        return make_response(error[0], error[1])  
    
    user_id = event['path']['id']
    users_db = user_list()
    users_data  = users_db.users_data
    if user_id > len(users_data[0]):
        return make_response(404, 'User not found')

    user_info={}
    for key in users_data.keys():
        user_info[key] = users_data[key][user_id]

    return make_response(200, user_info)


def update_user_info(event=None, context=None):
    '''
    check if body is present 400
    check if id was given 400
    load users on pandas
    check if user exists 404
    get user data
    change user data
    save data back to s3
    200
    '''
    user_params = ['name', 'age', 'gender', 'ownAuto', 'licence', 'vehicleType']

    if error := check_param(event, 'body'):
        return make_response(error[0], error[1])  

    update_params = event['body']
    if error := check_param(event['path'], 'id'):
        return make_response(error[0], error[1])  

    user_id = event['path']['id']
    users_db = user_list()
    users_data  = users_db.users_data
    if user_id > len(users_data[0]):
        return make_response(404, 'User not found')

    for key in users_data.keys():
        if key in update_params:
            users_data[key][user_id] = update_params[key]

    users_db.save_users()
    return make_response(200, f'User updated: {users_data["name"][user_id]}')


def get_terminal(event=None, context=None):
    '''
    load terminals on pandas
    check if terminal exists 404
    get terminal data
    return json of data
    200
    '''
    pass

def make_response(code, body):
    response = {
        "statusCode": code,
        "body": json.dumps(body)
    }
    return response


if __name__ == "__main__":
    new_users = {
        'name': [1,2,3],
        'age': [3,2,1]
    }
    x = pd.DataFrame(new_users)

    print(x.to_dict(orient='list'))

    # new_guy={
    #     'name': 9,
    #     'age': 0
    # }
    # x = x.append(new_guy, ignore_index=True)
    # print(x)
    # filters = {
    #     'name': 2,
    #     'age': 2
    # }
    # y = x
    # for k, v in filters.items():
    #     f = y[k]>=v
    #     y = y[f]
    #     print(y)
    
    # print(json.loads(x))

    # x = user_list()
    # print(x.users_data)
    # x.save_users()
    pass

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

    