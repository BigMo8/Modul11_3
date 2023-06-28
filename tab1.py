#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import plotly.graph_objects as go

#Tworzymy funkcję render_tab, która przyjmie za argument bazę danych. Będziemy potrzebowali bazy danych,
# aby określić domyślny zakres dat dla widgetu DatePickerRange.

#struktura layoutu:
# layout = html.Div([html.H1(),
            #html.Div([dcc.DatePickerRange()]),
            #html.Div([html.Div([dcc.Graph()]),html.Div([dcc.Graph()]
            #)]
            #)]
            #)

#SPRZEDAŻ GLOBALNA
def render_tab(df):

    layout = html.Div([html.H1('Sprzedaż globalna',style={'text-align':'center'}),
                        html.Div([dcc.DatePickerRange(id='sales-range',
                        start_date=df['tran_date'].min(),
                        end_date=df['tran_date'].max(),
                        display_format='YYYY-MM-DD')],style={'width':'100%','text-align':'center'}),
                        html.Div([html.Div([dcc.Graph(id='bar-sales')],style={'width':'50%'}),
                        html.Div([dcc.Graph(id='choropleth-sales')],style={'width':'50%'})],style={'display':'flex'})
                        ])

    return layout