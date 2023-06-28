#zakładka, która zawierać będzie dane dotyczące kanałów sprzedaży ('Store_type').
#klienci każdego z kanałów sprzedaży

#Store_type w transactions
#tran_date w transcations
#cust_id w transactions
#DOB, gender, country_code w customers
#country w country_codes

#docelowo: wykresy kołowe z podziałem na gender i DOB w kanałach sprzedaży

#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import plotly.graph_objects as go
