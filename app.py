# 일자별 지역 부동산 가격지수 산출함수

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from datetime import date
import datetime
import pandas as pd
import dash_table
import numpy as np
import pandas_datareader.data as web
import dash_bootstrap_components as dbc


df = pd.read_csv('C:/Users\ysj/PycharmProjects/property/전국부동산.csv', encoding='CP949')

start_date = '20180101'
end_date = '20210607'
dff = df[(df['구분'] >= start_date) & (df['구분'] <= end_date)]
dff.reset_index(drop=True)
dff = pd.melt(dff, id_vars=['구분'], var_name='지역', value_name='Index')
fig = px.line(dff, x='구분', y='Index', color = '지역')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H3("지역별 부동산 가격지수"),
    html.Br(),
    dcc.DatePickerRange(
        id="my-date-picker-range",
        min_date_allowed=date(2015, 1, 1),
        start_date_placeholder_text='20150110',
        end_date_placeholder_text='20210607',
        display_format='YYYYMMDD'
    ),
    html.Br(),
    html.Br(),
    dash_table.DataTable(
        id="datatable-interactivity",
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=15,
        page_current=0,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    ),
    html.Br(),
    html.Br(),
    dcc.Graph(
        style={'height': 600},
        id='my-graph',
        figure = fig
    )
])


# 입력된 Input으로 Output이 만들어지는 Call back 함수입니다.
# Input : DATE
# Output : 지역별 가격지수
@app.callback(
    Output('my-graph', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
def update_graph(start_date, end_date):
    dff = df[(df['구분'] >= start_date) & (df['구분'] <= end_date)]
    dff.reset_index(drop=True)
    dff = pd.melt(dff, id_vars=['구분'], var_name='지역', value_name='Index')
    fig = px.line(dff, x='구분', y='Index', color='지역')

    return fig



if __name__ == "__main__":
    app.run_server(debug=True, port=8030)