# Using plotly.express
from influxdb_client import InfluxDBClient, Point, Dialect, WriteOptions, WritePrecision
import plotly.express as px
import configparser
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import plotly.express as px
import os
from dotenv import load_dotenv
import time
import socket
load_dotenv()

client = None


def checknetstate(url, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((url, port))
    except Exception as err:
        return False
    if result == 0:
        return True
    else:
        return False
    sock.close()


def connect_db():
    # connect to database
    global client
    read_config = configparser.ConfigParser()
    while True:
        try:
            read_config.read("config/influx-configs")
            break
        except Exception as err:
            time.sleep(3)
            pass
    url = (read_config.get("default", "url")).strip(
        '"').replace('localhost', 'influxdb')
    while True:
        if checknetstate('influxdb', int(url.split(":")[-1])):
            break
        else:
            time.sleep(3)
    client = InfluxDBClient(
        url=url, token=read_config.get("default", "token").strip('"'), org=read_config.get("default", "org").strip('"'),
        verify_ssl=False, timeout=26000, ssl=False, debug=False)
    return client


def getDataFrame():
    client = connect_db()
    bucketname = os.getenv("bucketname")
    query = F'''
    from(bucket: "{bucketname}")
    |> range(start:-3000d, stop: now())
    '''
    df = client.query_api().query_data_frame(
        org=os.getenv('org'), query=query)
    return df


if __name__ == "__main__":

    df = getDataFrame()

    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Dropdown(
            id="ticker",
            options=[{"label": '_value', "value": '_value'}],
            value='_value',
            clearable=False,
        ),
        dcc.Graph(id="time-series-chart"),
        dcc.Interval(
            id='interval-component',
            interval=3*1000,  # in milliseconds
            n_intervals=0
        )
    ])

    @app.callback(Output('time-series-chart', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def update_metrics(n):
        if(n == 0):
            PreventUpdate()
        df = getDataFrame()
        fig = px.line(df, x='_time', y='_value')
        return fig

    app.run_server(debug=True)
