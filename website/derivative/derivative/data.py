import pandas as pd
import datetime
import os
from WindPy import w

import const
import utils

w.start()

def get_option_list():
    df = pd.read_excel(const.OPT_LIST, index_col=0)
    return df

def download_option_information(option_code, start_date, end_date):
    fname = '%s/%s.xlsx'%(const.OPTION_DIR, option_code)
    '''
    if os.path.exists(fname):
        return
    '''
    data = w.wsd(option_code, "oi,close", start_date, end_date)
    df = utils.wind2df(data)
    df.to_excel(fname)

def download_options_history(df):
    yesterday = datetime.datetime.today() - datetime.timedelta(1)
    for index in df.index:
        wind_code = str(index) + '.SH'
        start_date = df.loc[index, 'listed_date']
        end_date = df.loc[index, 'exercise_date']
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        if yesterday < end_date:
            end_date = yesterday
        print wind_code
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        download_option_information(wind_code, start_date, end_date)