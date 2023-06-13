import pandas as pd
import datetime as dt
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


class db:
    def __init__(self):
        self.transactions = db.transation_init()
        self.cc = pd.read_csv(r'db\country_codes.csv',index_col=0)
        self.customers = pd.read_csv(r'db\customers.csv',index_col=0)
        self.prod_info = pd.read_csv(r'db\prod_cat_info.csv')



@staticmethod
def transation_init():
    transactions = pd.DataFrame()
    src = r'db\transactions'
    for filename in os.listdir(src):
        transactions = transactions.append(pd.read_csv(os.path.join(src,filename),index_col=0))

    def convert_dates(x):
        try:
            return dt.datetime.strptime(x,'%d-%m-%Y')
        except:
            return dt.datetime.strptime(x,'%d/%m/%Y')

    transactions['tran_date'] = transactions['tran_date'].apply(lambda x: convert_dates(x))

    return transactions
