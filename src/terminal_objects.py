from src.helpers import s3
from src.helpers.verify import check_file
import pandas as pd
from datetime import datetime

class terminal_traffic(object):
    def __init__(self, terminal_id, ini_date, end_date):
        self.terminal_id = terminal_id
        if not (ini_date or end_date):
            ini_date = datetime.utcnow()
            end_date = datetime.utcnow()
            
        self.ini_date = ini_date
        self.end_date = end_date

        self.terminal_data = {
            'traffic': {},
            'meta': {
                'vehicleType':[
                    'Unknown',
                    'Caminhão 3/4',
                    'Caminhão Toco',
                    'Caminhão Truck',
                    'Caminhão Simples',
                    'Carreta Eixo',
                ]}
        }
        user_params = ['timestamp', 'user', 'origin', 'destination', 'loaded', 'vehicleType']

    def _load_data(self):
        dl_path = s3.data_lake_name()
        if (data := check_file(f'terminal/{self.terminal_id}/{dl_path}/{}')):
            self.terminal_data = data        
        self.terminal_df = pd.DataFrame(self.terminal_data['terminals'])
    
    def save_data(self):
        s3.s3_upload(self.users_data, 'users/user_list.json')
class terminal_list(object):
    def __init__(self):
        '''
        This class would be to manage data from terminals.
        But since in this demo we'll be working with a single terminal, 
        this class is just a waypoint for expansion.
        '''
        self.terminal_data = {
            'terminals': {},
            'meta': {}
        }
    def _load_terminal(self):
        pass

    def save_terminal(self):
        pass
        # s3.s3_upload(self.users_data, 'users/user_list.json')

    def add_terminal(self, new_user):
        pass
        #  self.users_df = self.users_df.append(new_user, ignore_index=True)
        #  self.users_data['users'] = self.users_df.to_dict(orient='list')
    
    def filter_terminals(self, masks):
        pass
        # filtered_df = self.users_df
        # for key, value in masks.items():
        #     mask = self.users_df[key == value]
        #     masked_df = filtered_df[mask]
        #     if masked_df.size==0:
        #         break
        # return masked_df.to_dict(orient='list')
    