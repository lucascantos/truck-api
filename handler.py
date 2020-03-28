import json
from src.user_objects import user_list
from src.terminal_objects import terminal_traffic
from src.helpers.verify import check_param, check_object, make_response
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
        body['users'] = users_db.filter_users(filter_params)
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
    if error := check_object(user_id, users_db.users_data):
        return error
        
    user_info = users_db.get_users(user_id)

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
    if error := check_param(event, 'body'):
        return make_response(error[0], error[1])  

    update_params = event['body']
    if error := check_param(event['path'], 'id'):
        return make_response(error[0], error[1])  

    user_id = event['path']['id']
    users_db = user_list()
    users_data  = users_db.users_data    

    if error := check_object(user_id, users_data):
        return error

    for key in users_data.keys():
        if key in update_params:
            users_data[key][user_id] = update_params[key]

    users_db.save_users()
    return make_response(200, f'User updated: {users_data["name"][user_id]}')


def get_terminal_info(event=None, context=None):
    allowed_params=['loaded']

    if error := check_param(event['path'], 'terminal_id'):
        return make_response(error[0], error[1])  
    terminal_id = event['path']['terminal_id']
    # if error := check_object(user_id, terminal_list().terminal_id):
    #     return error
    if terminal_id != 0:
        return make_response(404, 'Not Found') 
        
    if check_param(event, 'queryStringParameters'):
        filter_params = event['queryStringParameters']
        if not ('ini_date' or 'end_date'):
            filter_params['ini_date'] = None
            filter_params['end_date'] = None 
        
    traffic_db = terminal_traffic(terminal_id, filter_params['ini_date'], filter_params['end_date'])
    filter_params.pop('ini_date')
    filter_params.pop('end_date')

    body = traffic_db.terminal_data
    if len(filter_params) > 0:
        if 'groupByVehicle' in filter_params:
            body = traffic_db.group_data('vehicleType', traffic_db.terminal_data['meta']['vehicleType'])
        else:
            body['traffic'] = traffic_db.filter_data(filter_params)
    return make_response(200, body)  

    '''
    load terminals on pandas
    check if terminal exists 404
    get terminal data
    return json of data
    200
    '''
def add_terminal_traffic(event=None, context=None):    
    traffic_params = ['user', 'origin', 'destination', 'loaded', 'vehicleType']

    if error := check_param(event, 'body'):
        return make_response(error[0], error[1])  

    for param in traffic_params:        
        if error := check_param(event['body'], param):
            return make_response(error[0], error[1])  
    
    if error := check_param(event['path'], 'terminal_id'):
        return make_response(error[0], error[1])  
    terminal_id = event['path']['terminal_id']
    if terminal_id != 0:
        return make_response(404, 'Not Found')
          
    new_traffic_params = json.loads(event['body'])
    traffic_db = terminal_traffic(terminal_id, None, None)
    traffic_db.add_data(new_traffic_params)
    traffic_db.save_data()

    return make_response(201, f'New traffic added: {new_traffic_params["name"]}')

def get_terminal_users(event=None, context=None):

    if error := check_param(event['path'], 'terminal_id'):
        return make_response(error[0], error[1])  
    terminal_id = event['path']['terminal_id']
    if terminal_id != 0:
        return make_response(404, 'Not Found')
    
    if check_param(event, 'queryStringParameters'):
        filter_params = event['queryStringParameters']
        if not ('ini_date' or 'end_date'):
            filter_params['ini_date'] = None
            filter_params['end_date'] = None 

    traffic_db = terminal_traffic(terminal_id, filter_params['ini_date'], filter_params['end_date'])
    pass



if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    x = {
        'name': [1,2,3],
        'age': [3,2,1],
        'gender': [1,2,1]
    }
    y = {
        'name': [4,4],
        'age': [1,2],

    }

    '''
    header:{
        unique_value{

        }
    }
    '''
    df = pd.DataFrame(x)
    headers = ['df.columns']
    print(headers)
    if isinstance(headers, (list, object)):
        if headers in df.columns:

            print('nice')
    print(df[headers].to_dict(orient='list'))

    # print(x.to_dict(orient='list'))
    # y = np.array(x['name'])
    # print(y[[0,1]])
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

    