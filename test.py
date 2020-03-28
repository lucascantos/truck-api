

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
    y = {"name": "AKAK"}
    i = "0"

    for key in y.keys():
        print(key)
        if key in x.keys():
            x[key][i] = y[key]
    
    print(x)


    # id_list=[0]
    # masked_df = {}
    # pd.date_range()
    # for key in x.keys():        
    #     masked_df[key] = list(np.array(x[key])[id_list])

    #     print(masked_df)
    # for key, value in y.items():
    #     print(key,value)
    #     mask = x['name']==2
    # df = pd.DataFrame(x)
    # headers = ['df.columns']
    # print(headers)
    # if isinstance(headers, (list, object)):
    #     if headers in df.columns:

    #         print('nice')
    # print(df[headers].to_dict(orient='list'))

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