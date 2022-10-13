import dash
from dash import html
import plotly.graph_objects as go
from dash import dcc
from dash import dash_table
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import datetime
from datetime import datetime as dt
import config
import data_preparation
import grid_analyse

from datetime import date
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

config.df_symbol = data_preparation.record(config.init_symbol, config.init_date_string, config.init_interval)
config.df_symbol, config.df_grid = grid_analyse.get_grid_params(config.df_symbol, config.init_symbol, config.init_step_percent)

app = dash.Dash()

app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='InTrade Research - GRID DASHBOARD',
            style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
    html.H1(id='H2', children='Asset Grid Selection',
            style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),

    html.Div(id="group_asset_title", children=[
        html.Div(
            html.H1(id='H3', children='Start Date', style={'textAlign': 'left', 'marginTop': 40, 'marginBottom': 40}),
            style={'display': 'inline-block', 'width': '20%'}, ),
        html.Div(
            html.H1(id='H4', children='Symbols', style={'textAlign': 'left', 'marginTop': 40, 'marginBottom': 40}),
            style={'display': 'inline-block', 'width': '20%'}, ),
        html.Div(
            html.H1(id='H5', children='Intervals', style={'textAlign': 'left', 'marginTop': 40, 'marginBottom': 40}),
            style={'display': 'inline-block', 'width': '20%'}, ),
        html.Div(
            html.H1(id='H6', children='GridSteps', style={'textAlign': 'left', 'marginTop': 40, 'marginBottom': 40}),
            style={'display': 'inline-block', 'width': '20%'}, ),
    ], style={'display': 'inline-block', 'width': '100%'}
             ),

    html.Div(id='output-container-date-picker-single'),

    html.Div(id="group_asset_dropdown", children=[
        html.Div(
            dcc.DatePickerSingle(
                id='my-date-picker-single',
                date=date(2022, 6, 1)
            ),
            style={'display': 'inline-block', 'width': '20%'}, ),
        html.Div(
            dcc.Dropdown(id='dropdown_interval',
                         options=config.lst_intervals,
                         value=config.lst_intervals[0]),
            style={'display': 'inline-block', 'width': '20%'}, ),
        html.Div(
            dcc.Dropdown(id='dropdown_symbol',
                         options=config.lst_default_symbols,
                         value=config.lst_default_symbols[0]),
            style={'display': 'inline-block', 'width': '20%'}, ),
        html.Div(
            dcc.Dropdown(id='dropdown_step',
                         options=config.lst_default_step,
                         value=config.lst_default_step[1]),
            style={'display': 'inline-block', 'width': '20%'}, ),
    ], style={'display': 'inline-block', 'width': '100%'}
             ),
    dcc.Graph(id="graph_zone"),
    dcc.Graph(id='graph_bar'),
    dcc.Graph(id="graph_close"),

    dcc.Slider(0, 100, 5,
               value=0,
               id='my-slider'
               ),
    html.Div(id='slider-output-container'),

    dcc.Graph(id='graph_bar_reduced'),
    dcc.Graph(id="graph_zone_reduced"),

    html.Div(
        dcc.Dropdown(id='dropdown_grid_table',
                     options=['df_grid', 'df_symbol'],
                     value='df_grid',
        style={'display': 'inline-block', 'width': '30%'}, ),
    ),

    dash_table.DataTable(id='grid_table',
                         style_cell={'textAlign': 'center'})

])

@app.callback(
    Output("graph_bar", "figure"),
    Output("graph_zone", "figure"),
    Output("graph_close", "figure"),
    [Input('dropdown_step', 'value'),
    Input('dropdown_symbol', 'value'),
    Input('dropdown_interval', 'value'),
    Input('my-date-picker-single', 'date')]
)
def update_zone_graph(step, symbol, interval, date_value):
    config.init_step_percent = step
    config.init_symbol = symbol
    config.init_interval = interval
    if date_value is not None:
        config.init_date_string = date_value
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%Y-%m-%d')

    config.df_symbol = data_preparation.record(config.init_symbol, config.init_date_string, config.init_interval)
    config.df_symbol, config.df_grid = grid_analyse.get_grid_params(config.df_symbol, config.init_symbol, config.init_step_percent)

    figure_zone = px.scatter(config.df_symbol, y='close_zone', height=400, text='close_zone')
    figure_close = px.line(config.df_symbol, y='close', height=400)
    figure_bar = px.bar(config.df_grid, y='sum', height=400, text='sum')

    return figure_zone, figure_bar, figure_close

@app.callback([Output(component_id='grid_table', component_property='data'),
               Output(component_id='grid_table', component_property='columns')],
               Input("dropdown_grid_table", "value"))
def update_table_trades(value):
    if value == 'df_grid':
        df = config.df_grid.copy()
        df['zone'] = df.index
        df = df.iloc[:, [3, 0, 1, 2]]
    else:
        df = config.df_symbol.copy()

    columns = [{'name': col, 'id': col} for col in df.columns]
    data = df.to_dict(orient='records')
    return data, columns

@app.callback(
    Output('slider-output-container', 'children'),
    Output("graph_bar_reduced", "figure"),
    Output("graph_zone_reduced", "figure"),
    Input('my-slider', 'value'))
def update_output(value):
    df_symbol_filtered = config.df_symbol.copy()
    df_grid_filtered = config.df_grid.copy()

    max_symbol = max(df_symbol_filtered['close_zone'])
    max_grid = max(df_grid_filtered['sum'])

    # 100 -> max
    # val -> ...       ... = max * val / 100
    symbol_threshold = max_symbol * value / 100
    grid_threshold = max_grid * value / 100

    df_symbol_filtered.loc[df_symbol_filtered["close_zone"] <= symbol_threshold, "close_zone"] = 0
    df_symbol_filtered["close_zone"] = df_symbol_filtered["close_zone"] * -1  # Modif CEDE work around -1

    df_grid_filtered.loc[df_grid_filtered["sum"] <= grid_threshold, "sum"] = 0

    figure_zone = px.scatter(df_symbol_filtered, y='close_zone', height=400, text='close_zone')
    figure_bar = px.bar(df_grid_filtered, y='sum', height=400, text='sum')

    return 'You have selected "{}"'.format(value), figure_bar, figure_zone

if __name__ == '__main__':
    app.run_server()