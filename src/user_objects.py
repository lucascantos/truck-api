from src.helpers import s3
from src.helpers.verify import check_file
import pandas as pd
import numpy as np

class user_list(object):
    def __init__(self):
        self.users_data = {}

        user_params = ['name', 'age', 'gender', 'ownAuto', 'licence']
        for param in user_params:
            self.users_data[param] = []
        self._load_users()
        self.users_df = pd.DataFrame(self.users_data)

    def _load_users(self):
        if (data := check_file('users/user_list.json')):
            self.users_data = data

    def save_users(self):
        s3.s3_upload(self.users_data, 'users/user_list.json')

    def add_user(self, new_user):
         self.users_df = self.users_df.append(new_user, ignore_index=True)
         self.users_data = self.users_df.to_dict(orient='list')
    
    def filter_users(self, mask_dict, headers=None):
        filtered_df = self.users_df
        for key, value in mask_dict.items():
            mask = self.users_df[key]==value
            masked_df = filtered_df[mask]
            if masked_df.size==0:
                break
        if not headers or not isinstance(headers, (list, object)):
            headers = masked_df.columns
        return masked_df[headers].to_dict(orient='list')
    
    def get_users(self, id_list):
        if not isinstance(id_list, list):
            id_list = [id_list]

        masked_df = {}
        for key in self.users_data.keys():     
            x = np.array(self.users_data[key])  
            print(x)    
            masked_df[key] = list(x[id_list])

        return masked_df

    @property
    def data(self):
        return {
            'users': self.users_data,
            'meta': {}
        }
    
            
