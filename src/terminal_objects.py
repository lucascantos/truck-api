from src.helpers import s3
from src.helpers.verify import check_file
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

class terminal_traffic(object):
    def __init__(self, terminal_id, ini_date, end_date):
        self.terminal_id = terminal_id
        if not (ini_date or end_date):
            ini_date = datetime.utcnow()
            end_date = datetime.utcnow()
            
        self.ini_date = ini_date
        self.end_date = end_date

        self.terminal_data = {
            'info': {}, #Filled with terminal data
            'traffic': {}, #Filled with in/ou of trucks
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
        traffic_params = ['timestamp', 'user', 'origin', 'destination', 'loaded', 'vehicleType']

        for param in traffic_params:
            self.terminal_data['traffic'][param] = []
        
        for date in pd.daterange(self.ini_date, self.end_date):
            self._load_data(date)
        self.terminal_df = pd.DataFrame(self.terminal_data['traffic'])

    def _load_data(self, date):
        filename = date.strftime(f'terminal_{self.terminal_id}_%Y%m%d.json')
        self.filepath = f'{s3.data_lake_name(date)}/{filename}'
        if (data := check_file(f'terminals/{self.terminal_id}/{self.filepath}')):
            for key, value in data.items():
                self.terminal_data['traffic'][key] += value
    
    def save_data(self):
        s3.s3_upload(self.terminal_data['traffic'], f'terminals/{self.filepath}')

    def add_data(self, new_traffic):
        new_traffic['timestamp'] = datetime.utcnow()
        self.terminal_df = self.terminal_df.append(new_traffic, ignore_index=True)
        self.terminal_data['users'] = self.terminal_df.to_dict(orient='list')

    def filter_data(self, mask_list):
        filtered_df = self.terminal_df
        for key, value in mask_list.items():
            mask = self.terminal_df[key == value]
            masked_df = filtered_df[mask]
            if masked_df.size==0:
                break
        return masked_df.to_dict(orient='list')

        
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

    def add_terminal(self, new_terminal):
        pass
    
    def filter_terminals(self, mask_list):
        pass
        # filtered_df = self.users_df
        # for key, value in masks.items():
        #     mask = self.users_df[key == value]
        #     masked_df = filtered_df[mask]
        #     if masked_df.size==0:
        #         break
        # return masked_df.to_dict(orient='list')
    