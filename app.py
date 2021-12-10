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
    html.H2(children="Covid-19 Dashboard"),
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
    df['prev_cases'] = df.groupby('state')['cases'].shift().fillna(0)
    df['new cases'] = df['cases'] - df['prev_cases']
    df_last_30 = df[df["state"] == states].iloc[-1:-31:-1][::-1]

    fig = px.bar(df_last_30, x="date", y="new cases")
    
    fig.update_layout(
    plot_bgcolor="white",
    # title="Number of Cases per State",
    xaxis_title="Date",
    yaxis_title="Number of New Cases"
    )

    return fig

app.run_server(debug=True, host="0.0.0.0")