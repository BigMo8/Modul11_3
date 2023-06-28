#zakładka, która zawierać będzie dane dotyczące kanałów sprzedaży ('Store_type').
#w jakich dniach tygodnia dokonuje się najwięcej sprzedaży w zależności od kanału sprzedaży

#Store_type w transactions
#tran_date w transcations
#cust_id w transactions
#DOB, gender, country_code w customers
#country w country_codes

#doeclowo: wykres słupkowy z podziałem na dni tygodnia i kanały sprzedaży

#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import plotly.graph_objects as go

#KANAŁY SPRZEDAŻY
def render_tab(df):

    grouped = df[df['total_amt']>0].groupby('Store_type')['total_amt'].sum()
    fig = go.Figure(data=[go.Pie(labels=grouped.index,values=grouped.values)],layout=go.Layout(title='Udział kanałów sprzedaży'))

#struktura layoutu:
# layout = html.Div([html.H1(),
#            html.Div([html.Div([dcc.Graph(),
#                        html.Div([dcc.Dropdown(),dcc.Graph()]),
#                    html.Div(id='temp-out')
#                        ])

    layout = html.Div([html.H1('Kanały sprzedaży',style={'text-align':'center'}),
                        html.Div([html.Div([dcc.Graph(id='pie-Store-type',figure=fig)],style={'width':'50%'}),
                        html.Div([dcc.Dropdown(id='Store-type_dropdown',
                                    options=[{'label':Store_type,'value':Store_type} for Store_type in df['Store_type'].unique()],
                                    value=df['Store_type'].unique()[0]),
                                    dcc.Graph(id='barh-Store-type')],style={'width':'50%'})],style={'display':'flex'}),
                                    html.Div(id='temp-out')
                        ])

    return layout