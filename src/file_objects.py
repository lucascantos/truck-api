from src.helpers import s3
from src.helpers.verify import check_file
class user_list(object):
    def __init__(self):
        self.users_data = {
            'users': {},
            'meta': {
                'vehicleType':[
                    'No Truck',
                    'Caminhão 3/4',
                    'Caminhão Toco',
                    'Caminhão Truck',
                    'Caminhão Simples',
                    'Carreta Eixo',
                ]}
        }
        user_params = ['name', 'age', 'gender', 'ownAuto', 'licence', 'vehicleType']
        for param in user_params:
            self.users_data['users'][param] = []

    def load_users(self):
        if (data := check_file('users/user_list.json')):
            self.users_data = data

    def save_users(self):
        s3.s3_upload(self.users_data, 'users/user_list.json')

class terminal_list(object):
    def __init__(self):
        pass

if __name__ == "__main__":
    x = user_list()
    print(x.users_data)
    pass