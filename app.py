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
states = sorted(df.state.unique())

app.layout = html.Div([
    html.H2(children="Number of Cases per State"),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,
        n_intervals=0
    ),
     
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in states],
        value=states[0],
        clearable=False,
    ),

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

def bar_plot(n_clicks, states):
    df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    df['last_week_cases'] = df['cases'].rolling(7).sum()
    mask = df["state"] == states
    df_last_week = df[mask][::-1]
    fig = px.area(df_last_week, x="date", y="last_week_cases")
    fig.update_layout(plot_bgcolor="white") 
    return fig

app.run_server(debug=True, host="0.0.0.0")