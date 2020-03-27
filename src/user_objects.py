from src.helpers import s3
from src.helpers.verify import check_file
import pandas as pd
import numpy as np

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
        self.users_df = pd.DataFrame(self.users_data['users'])

    def save_users(self):
        s3.s3_upload(self.users_data, 'users/user_list.json')

    def add_user(self, new_user):
         self.users_df = self.users_df.append(new_user, ignore_index=True)
         self.users_data['users'] = self.users_df.to_dict(orient='list')
    
    def filter_users(self, mask_dict):
        filtered_df = self.users_df
        for key, value in mask_dict.items():
            mask = self.users_df[key == value]
            masked_df = filtered_df[mask]
            if masked_df.size==0:
                break
        return masked_df.to_dict(orient='list')
    
    def get_users(self, id_list):
        masked_df = {}
        for key in self.users_data.keys():
            masked_df[key] = list(np.array(self.users_data[key])[id_list])
        
        return masked_df

    
            
