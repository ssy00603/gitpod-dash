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

server = app.server

df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
states = sorted(df.state.unique())
days = ['last 7 days', 'last 14 days', 'last 30 days']

app.layout = html.Div([
    # Add title
    html.H2(children="Covid-19 Dashboard"),

    # Add live date
    dcc.Interval(
        id='interval-component',
        interval=100000,
        n_intervals=0
    ),

    # Add tabs
    dcc.Tabs(id="tabs-inline", value='tab-1', children=[
        # Add tab of New Cases
        dcc.Tab(label='New Cases by States', value='tab-1', children=[
            # Choose states 
            dcc.Dropdown(
                id="dropdown",
                options=[{"label": x, "value": x} for x in states],
                value=states[0],
                clearable=False,
            ),
            # Choose day intervals
            dcc.Dropdown(
                id="dropdown-days",
                options=[{"label": x, "value": x} for x in days],
                value=days[0],
                clearable=False,
            ),
            # Display bar plot
            dcc.Graph(id="bar-chart-new")
        ]),

        # Add tab of Total Cases
        dcc.Tab(label='Total Cases', value='tab-2', children=[
            # Display bar plot
            dcc.Graph(id="bar-chart-total")
        ]),

        # Add tab of Deaths
        dcc.Tab(label='Deaths', value='tab-3', children=[
            # Display bar plot
            dcc.Graph(id="bar-chart-death")
        ])]),

        # Display map
        dcc.Graph(id="map-vaccine")

])


@app.callback(
    Output('bar-chart-new', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input("dropdown", "value"),
    Input("dropdown-days", "value"))

def bar_plot_days(n_clicks, states, days):
    df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    # Add previous cases column
    df['prev_cases'] = df.groupby('state')['cases'].shift().fillna(0)
    # Add new cases column
    df['new cases'] = df['cases'] - df['prev_cases']

    # Choose display day interval
    if days == 'last 7 days':
        df = df[df["state"] == states].iloc[-1:-8:-1][::-1]
    if days == 'last 14 days':
        df = df[df["state"] == states].iloc[-1:-15:-1][::-1]
    else:
        df = df[df["state"] == states].iloc[-1:-31:-1][::-1]

    # Plot line with bar plot
    fig = px.line(df, x="date", y="new cases")
    fig.add_bar(x=df["date"], y=df["new cases"], marker=dict(color="Blue", opacity=0.3), showlegend=False)

    fig.update_layout(
    plot_bgcolor="white",
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
    
    # Plot line with bar plot
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
    
    # Plot line with bar plot
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

    # Plot map
    fig = px.choropleth(df_state_vaccine,
                        locations='Abbreviation',
                        color='total_vaccinations',
                        color_continuous_scale='Teal',
                        hover_name='State',
                        locationmode='USA-states',
                        labels={'total_vaccinations':'Number of Vaccinations'},
                        scope='usa')

    # Hide line between states
    fig.update_traces(marker_line_width=0)

    # Add State abbreviation
    fig.add_scattergeo(locations=df_state_vaccine['Abbreviation'],
                        locationmode='USA-states',
                        text=df_state_vaccine['Abbreviation'],
                        mode='text',
                        hoverinfo='none')

    fig.update_layout(
        title={'text':'Total Vaccinations by State',
            'xanchor':'center',
            'yanchor':'top',
            'x':0.5})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")