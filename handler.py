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
    print(event)
    if not check_param(event, 'queryStringParameters'):
        filter_params = event['queryStringParameters']
        print(filter_params)
        users_db.users_data = users_db.filter_users(filter_params)
    
    body = users_db.data
    return make_response(200, body)


def add_user(event=None, context=None):
    '''
    Check if parameters are right [name, age, gender, ownAuto, licence, vehicleType] 400
    Load users on pandas
    Include data do table
    Save users back to s3
    201
    '''
    user_params = ['name', 'age', 'gender', 'ownAuto', 'licence']

    if error := check_param(event, 'body'):
        return make_response(error[0], error[1])  

    new_user_params = json.loads(event['body'])

    for param in user_params:        
        if error := check_param(new_user_params, param):
            return make_response(error[0], error[1])  
    
   

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
    if error := check_param(event['pathParameters'], 'user_id'):
        return make_response(error[0], error[1])  
    try:
        user_id = int(event['pathParameters']['user_id'])
    except:
        return (make_response(400, 'Id must be interger'))

    users_db = user_list()    
    if error := check_object(user_id, users_db.users_data):
        return error
        
    user_info = users_db.get_users([user_id])

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

    update_params = json.loads(event['body'])
    if error := check_param(event['pathParameters'], 'user_id'):
        return make_response(error[0], error[1])  

    try:
        user_id = int(event['pathParameters']['user_id'])
    except:
        return (make_response(400, 'Id must be interger'))
        
    users_db = user_list()
    users_data  = users_db.users_data    

    if error := check_object(user_id, users_data):
        return error

    for key in update_params.keys():
        if key in users_data.keys():
            print(key)
            print(type(user_id), user_id)
            users_data[key][user_id] = update_params[key]

    users_db.save_users()
    return make_response(200, f'User updated: {users_data["name"][user_id]}')


def get_terminal_info(event=None, context=None):
    allowed_params=['loaded']

    if error := check_param(event['pathParameters'], 'terminal_id'):
        return make_response(error[0], error[1])  
    try:
        terminal_id = int(event['pathParameters']['terminal_id'])
    except:
        return (make_response(400, 'Id must be interger'))

    # if error := check_object(user_id, terminal_list().terminal_id):
    #     return error
    if terminal_id != 0:
        return make_response(404, 'Not Found') 
        
    if not check_param(event, 'queryStringParameters'):
        filter_params = event['queryStringParameters']
    else:
        filter_params = {}

    if not ('ini_date' or 'end_date') in filter_params:
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
    new_traffic_params = json.loads(event['body'])

    for param in traffic_params:        
        if error := check_param(new_traffic_params, param):
            return make_response(error[0], error[1])  
    
    if error := check_param(event['pathParameters'], 'terminal_id'):
        return make_response(error[0], error[1])  

    try:
        terminal_id = int(event['pathParameters']['terminal_id'])
    except:
        return (make_response(400, 'Id must be interger'))

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

    try:
        terminal_id = int(event['pathParameters']['terminal_id'])
    except:
        return (make_response(400, 'Id must be interger'))

    if terminal_id != 0:
        return make_response(404, 'Not Found')
    
    if check_param(event, 'queryStringParameters'):
        filter_params = event['queryStringParameters']
        if not ('ini_date' or 'end_date'):
            filter_params['ini_date'] = None
            filter_params['end_date'] = None 

    traffic_db = terminal_traffic(terminal_id, filter_params['ini_date'], filter_params['end_date'])
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


    