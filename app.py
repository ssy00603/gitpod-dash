import dash
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import dash_table


app = dash.Dash(__name__)
df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
states = sorted(df.state.unique())
days = ['last 7 days', 'last 14 days', 'last 30 days']

app.layout = html.Div([
    html.H2(children="Covid-19 Dashboard"),

    dcc.Interval(
        id='interval-component',
        interval=100000,
        n_intervals=0
    ),


    dcc.Tabs(id="tabs-inline", value='tab-1', children=[
        dcc.Tab(label='New Cases by States', value='tab-1', children=[
            dcc.Dropdown(
                id="dropdown",
                options=[{"label": x, "value": x} for x in states],
                value=states[0],
                clearable=False,
            ),

            dcc.Dropdown(
                id="dropdown-days",
                options=[{"label": x, "value": x} for x in days],
                value=days[0],
                clearable=False,
            ),

            dcc.Graph(id="bar-chart-new")
        ]),

        dcc.Tab(label='Total Cases', value='tab-2', children=[
            dcc.Graph(id="bar-chart-total")
        ]),

        dcc.Tab(label='Deaths', value='tab-3', children=[
            dcc.Graph(id="bar-chart-death")
        ])]),

        dcc.Graph(id="map-vaccine"),
    # html.H4(children="States with Most New Cases Yestarday"),

    # dash_table.DataTable(
    # id='df_state_vaccine',
    # columns=[{"name": i, "id": i} for i in ['state', 'new cases']],
    # data=df.to_dict('records'))

])


@app.callback(
    Output('bar-chart-new', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input("dropdown", "value"),
    Input("dropdown-days", "value"))

def bar_plot_days(n_clicks, states, days):
    df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    df['prev_cases'] = df.groupby('state')['cases'].shift().fillna(0)
    df['new cases'] = df['cases'] - df['prev_cases']
    if days == 'last 7 days':
        df = df[df["state"] == states].iloc[-1:-8:-1][::-1]
    if days == 'last 14 days':
        df = df[df["state"] == states].iloc[-1:-15:-1][::-1]
    else:
        df = df[df["state"] == states].iloc[-1:-31:-1][::-1]

    fig = px.line(df, x="date", y="new cases")
    fig.add_bar(x=df["date"], y=df["new cases"], marker=dict(color="Blue", opacity=0.3), showlegend=False)

    fig.update_layout(
    plot_bgcolor="white",
    # title="Number of Cases per State",
    xaxis_title="Date",
    yaxis_title="Number of New Cases"
    )

    return fig


@app.callback(
    Output('bar-chart-total', 'figure'),
    Input('interval-component', 'n_intervals'))

def bar_plot_total(n_clicks):
    df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    df = df.groupby('date').sum().reset_index()
    
    fig = px.line(df, x="date", y="cases")
    fig.add_bar(x=df["date"], y=df["cases"], marker=dict(color="Blue", opacity=0.3), showlegend=False)

    fig.update_layout(
    plot_bgcolor="white",
    xaxis_title="Date",
    yaxis_title="Number of Total Cases"
    )

    return fig


@app.callback(
    Output('bar-chart-death', 'figure'),
    Input('interval-component', 'n_intervals'))

def bar_plot_death(n_clicks):
    df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    df = df.groupby('date').sum().reset_index()
    
    fig = px.line(df, x="date", y="deaths")
    fig.add_bar(x=df["date"], y=df["deaths"], marker=dict(color="Blue", opacity=0.3), showlegend=False)

    fig.update_layout(
    plot_bgcolor="white",
    xaxis_title="Date",
    yaxis_title="Number of Death"
    )

    return fig

@app.callback(
    Output('map-vaccine', 'figure'),
    Input('interval-component', 'n_intervals'))

def map_vaccine(n):
    df_vaccine = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv')
    df_vaccine = df_vaccine[['date', 'location', 'total_vaccinations']]
    df_vaccine = df_vaccine.groupby('location').sum().reset_index()

    df_state_code = pd.read_csv('https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv')

    df_state_vaccine = df_state_code.merge(df_vaccine, left_on='State', right_on='location')
    df_state_vaccine = df_state_vaccine[['State', 'Abbreviation', 'total_vaccinations']]

    fig = px.choropleth(df_state_vaccine,
                        locations='Abbreviation',
                        color='total_vaccinations',
                        color_continuous_scale='Teal',
                        hover_name='State',
                        locationmode='USA-states',
                        labels={'total_vaccinations':'Number of Vaccinations'},
                        scope='usa')

    fig.update_traces(marker_line_width=0)

    fig.update_layout(
        title={'text':'Total Vaccinations by State',
            'xanchor':'center',
            'yanchor':'top',
            'x':0.5})

    return fig

# @app.callback(
#     Output('table', 'data'),
#     Input('interval-component', 'n_intervals'))

# def update_table(n):
#     today = datetime.date.today()
#     yestarday = str(today - datetime.timedelta(days=1))

#     df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
#     df['prev_cases'] = df.groupby('state')['cases'].shift().fillna(0)
#     df['new cases'] = df['cases'] - df['prev_cases']

#     df_yes = df[df['date'] == yestarday]
#     df_yes = df_yes[['state', 'new cases']].sort_values(by=['new cases'], ascending=False).head()
#     return df_yes.to_dict('records')

app.run_server(debug=True, host="0.0.0.0")