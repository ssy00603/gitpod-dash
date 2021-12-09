import dash
import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dash_table


app = dash.Dash(__name__)
df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
days = df.date.unique()[::-1]

app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=1*1000,
        n_intervals=0
    ),
     
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in days],
        value=days[0],
        clearable=False,
    ),

    dcc.Graph(id="bar-chart"),
    
    dcc.Graph(id="bar-chart")
    # dash_table.DataTable(
    # id='table',
    # columns=[{"name": i, "id": i} for i in df.columns],
    # data=df.to_dict('records'))

])


@app.callback(
    Output('bar-chart', 'figure'),
    Input('interval-component', 'n_intervals'),
    [Input("dropdown", "value")])

def bar_plot(n_clicks, day):
    df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    mask = df["date"] == day
    fig = px.bar(df[mask], x="state", y="cases")
    return fig


@app.callback(
    Output('bar-chart', 'figure'),
    Input('interval-component', 'n_intervals'))

def bar_plot(interval_component):
    df1 = pd.read_csv('https://raw.githubusercontent.com/bwang98/Data1010_project/main/toy_data.csv')
    df1 = df1.groupby('sex').count().reset_index()
    fig = px.bar(df1, x="sex", y="Unnamed: 0")
    return fig

app.run_server(debug=True, host="0.0.0.0")