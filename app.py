import os
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([html.H2('Hello World'),
                       dcc.Dropdown(
                           id = 'dropdown',
                           options = [{'label': i, 'value': i} for i in )])