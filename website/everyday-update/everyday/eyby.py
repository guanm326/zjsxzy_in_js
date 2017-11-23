from WindPy import w
import pandas as pd
import numpy as np
import datetime

import utils
import const

fname = '%s/EYBY.xlsx'%(const.DATA_DIR)

def download_data(start_date, end_date):
    w.start()
    data = w.wsd('000001.SH', 'pe_ttm', start_date, end_date)
    pe = utils.wind2df(data)
    data = w.wsd('065.CS', 'ytm_b', start_date, end_date, 'returnType=1')
    ytm = utils.wind2df(data)
    data = w.wsd('000001.SH', 'close', start_date, end_date)
    close = utils.wind2df(data)
    return pe, ytm, close

def update_data():
    df = pd.read_excel(fname, index_col=0)
    start_date = df.index[-1] + datetime.timedelta(1)
    end_date = datetime.datetime.today() - datetime.timedelta(1)
    if start_date < end_date and start_date.day != end_date.day:
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        print start_date, end_date
        pe, ytm, close = download_data(start_date, end_date)
        pe['ytm_b'] = ytm['ytm_b']
        pe['close'] = close['close']
        df = df.append(pe)
        df.to_excel(fname)

if __name__ == '__main__':
    update_data()
