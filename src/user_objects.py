from src.helpers import s3
from src.helpers.verify import check_file
import pandas as pd
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
        self._load_users()

    def _load_users(self):
        if (data := check_file('users/user_list.json')):
            self.users_data = data        
        self.users_df = pd.DataFrame(self.users_data)

    def save_users(self):
        s3.s3_upload(self.users_data, 'users/user_list.json')

    def add_user(self, new_user):
         self.users_df = self.users_df.append(new_user, ignore_index=True)
    
    def filter_users(self, masks):
        filtered_df = self.users_df
        for key, value in masks.items():
            mask = self.users_df[key == value]
            masked_df = filtered_df[mask]
            if masked_df.size==0:
                break
        return masked_df
            
