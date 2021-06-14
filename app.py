# 일자별 지역 부동산 가격지수 산출함수
# 데이터를 불러온다.
# Datapicker 기능으로 StartDate, EndDate를 입력한다.
# Dropbox 기능으로 지역을 설정할 수 있게 한다.


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


df = pd.read_excel('C:/Users/ysj/Desktop/전국부동산.xlsx')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H3("지역별 부동산 가격지수"),
    html.Br(),
    dcc.DatePickerRange(
        id="my-date-picker-range",
        min_date_allowed=date(2015, 1, 1),
        start_date_placeholder_text='2020-01-01',
        end_date_placeholder_text='2020-12-31',
        display_format='YYYYMMDD'
    ),
    html.Br(),
    dash_table.DataTable(
        id="datatable-interactivity",
        columns=[{"name": i, "id": i} for i in df.columns],
        data = df.to_dict("records"),
        page_size=10,  # number of rows visible per page
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
    dcc.Graph(
        style={'height': 600},
        id='my-graph'
    ),
    dcc.Graph(id='my-graph2', figure={}, clickData=None, hoverData=None)
])


# 입력된 Input으로 Output이 만들어지는 Call back 함수입니다.
# Input : TICKER, INDICATOR, DATE
# Output : df 중, TICKER, INDICATOR, DATE를 만족시키는 데이터의 그래프
@app.callback(
    Output('my-graph', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
def update_graph(indicator, start_date, end_date):
    dff = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    return {
        'data': [dict(
            x=dff['구분'],
            y=dff[dff['TICKER'] == TICKER_column_name][indicator],
            mode='line'
        )],
    }


if __name__ == "__main__":
    app.run_server(debug=True, port=8010)