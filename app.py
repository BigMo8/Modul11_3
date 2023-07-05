from datetime import datetime
import datetime as dt
import pandas as pd
import os
import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
#import dash_auth
import plotly.graph_objects as go
import tab1
import tab2

class db:
    def __init__(self):
        self.transactions = db.transation_init()
        self.cc = pd.read_csv(r'db\country_codes.csv',encoding='utf-8',index_col=0)
        self.customers = pd.read_csv(r'db\customers.csv',encoding='utf-8',index_col=0)
        self.prod_info = pd.read_csv(r'db\prod_cat_info.csv',encoding='utf-8')
        #pd.read_csv('file_name.csv', encoding='utf-8')
        
    @staticmethod
    def transation_init():
        transactions = pd.DataFrame()
        src = r'db\transactions'    
        for filename in os.listdir(src):
            #os.listdir() method in python is used to get the list of all files and directories in the specified directory
            transactions = transactions.append(pd.read_csv(os.path.join(src,filename),index_col=0, encoding='utf-8'))

        def convert_dates(x):
            try:
                return dt.strptime(x,"%d-%m-%Y")
            except:
                return dt.strptime(x,"%d/%m/%Y")
        #module datetime has no attr. strptime - wg dokumentacji pandas ma... 
        transactions['tran_date'] = transactions['tran_date'].apply(lambda x: convert_dates(x))
        return transactions

    #połączyć bazę z transakcjami z odpowiednimi kategoriami produktów, płcią klienta oraz krajem sprzedaży.
    def merge(self):
            #łączymy transakcje po kodzie produktu
        df = self.transactions.join(self.prod_info.drop_duplicates(subset=['prod_cat_code']).set_index('prod_cat_code')['prod_cat'],on='prod_cat_code',how='left')
            #łaczymy ww. tabelę df z prod_info po kolumnie prod_subcat_code
        df = df.join(self.prod_info.drop_duplicates(subset=['prod_sub_cat_code']).set_index('prod_sub_cat_code')['prod_subcat'],on='prod_subcat_code',how='left')
            #łączymy ww. tabelę df z tabelą customers
        df = df.join(self.customers.join(self.cc,on='country_code').set_index('customer_Id'),on='cust_id')
    
        self.merged = df
df = db()   
df.merge()

#Dash is running on http://127.0.0.1:8050/

#zewnętrzny layout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#dcc.Tab - zakładki, które umożliwią prostą nawigację po dashboardzie; Rodzic Tabs/tab-1 - dzieci tab-2, tab-3
app.layout = html.Div([html.Div([dcc.Tabs(id='tabs',value='tab-1',children=[
                            dcc.Tab(label='Sprzedaż globalna',value='tab-1'),
                            dcc.Tab(label='Produkty',value='tab-2')
                            ]),
                            html.Div(id='tabs-content')
                    ],style={'width':'80%','margin':'auto'})],
                    style={'height':'100%'})

#uruchamiamy serwer w trybie developerskim, który ułatwi nam wyłapanie powstałych błędów.

#CALLBACK - jest to technika programowania będąca odwrotnością wywołania funkcji; rejestrowanie funkcji do późniejszego wywołania; 
# CALLBACK odpowiedzialny za renderowanie zawartości aktywnej zakładki.Wywołają ją funkcje bblioteki w stsosownym czasie.

@app.callback(Output('tabs-content','children'),[Input('tabs','value')])
def render_content(tab):

    if tab == 'tab-1':
        return tab1.render_tab(df.merged)
    elif tab == 'tab-2':
        return tab2.render_tab(df.merged)


#W momencie, w którym aktywna jest zakładka pierwsza ('tab-1'), wywołuje funkcję render_tab z pliku tab1.py.
    ## tab1 callbacks

#Output jako pierwszy argument dekoratora callback: id komponentu, do którego ma być zwrócona wartość, atrybut który ma być uzupełniony 
# przez funkcję wskazaną niżej
#Input wskazuje na komponenty, z których pobierane są dane, i który strybut tych komponentówokreśli tę wartość 

@app.callback(Output('bar-sales','figure'),
    [Input('sales-range','start_date'),Input('sales-range','end_date')])
def tab1_bar_sales(start_date,end_date):

    truncated = df.merged[(df.merged['tran_date']>=start_date)&(df.merged['tran_date']<=end_date)]
    grouped = truncated[truncated['total_amt']>0].groupby([pd.Grouper(key='tran_date',freq='M'),'Store_type'])['total_amt'].sum().round(2).unstack()

    traces = []
    for col in grouped.columns:
        traces.append(go.Bar(x=grouped.index,y=grouped[col],name=col,hoverinfo='text',
        hovertext=[f'{y/1e3:.2f}k' for y in grouped[col].values]))

    data = traces
    fig = go.Figure(data=data,layout=go.Layout(title='Przychody',barmode='stack',legend=dict(x=0,y=-0.5)))

    return fig

#KARTOGRAM
@app.callback(Output('choropleth-sales','figure'),
        [Input('sales-range','start_date'),Input('sales-range','end_date')])
def tab1_choropleth_sales(start_date,end_date):

    truncated = df.merged[(df.merged['tran_date']>=start_date)&(df.merged['tran_date']<=end_date)]
    grouped = truncated[truncated['total_amt']>0].groupby('country')['total_amt'].sum().round(2)

    trace0 = go.Choropleth(colorscale='Viridis',reversescale=True,
                        locations=grouped.index,locationmode='country names',
                        z = grouped.values, colorbar=dict(title='Sales'))
    data = [trace0]
    fig = go.Figure(data=data,layout=go.Layout(title='Mapa',geo=dict(showframe=False,projection={'type':'natural earth'})))

    return fig

## tab2 callbacks   
@app.callback(Output('barh-prod-subcat','figure'),
        [Input('prod_dropdown','value')])
def tab2_barh_prod_subcat(chosen_cat):

    grouped = df.merged[(df.merged['total_amt']>0)&(df.merged['prod_cat']==chosen_cat)].pivot_table(index='prod_subcat',columns='Gender',values='total_amt',aggfunc='sum').assign(_sum=lambda x: x['F']+x['M']).sort_values(by='_sum').round(2)

    traces = []
    for col in ['F','M']:
        traces.append(go.Bar(x=grouped[col],y=grouped.index,orientation='h',name=col))

    data = traces
    fig = go.Figure(data=data,layout=go.Layout(barmode='stack',margin={'t':20,}))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)