import os
import pandas as pd
import numpy as np

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def get_grid_params(df_symbol, symbol, step_percent):
    close_max = df_symbol['close'].max()
    close_min = df_symbol['close'].min()
    close_delta = close_max - close_min
    print('close max: ', close_max)
    print('close min: ', close_min)
    print('close delta: ',close_delta)
    print("Q1 quantile of arr : ", np.quantile(df_symbol['close'].tolist(), .25))

    grid_step = int(close_delta * step_percent / 100)

    print('grid step: %', step_percent)
    print('grid step: $', grid_step)

    df_grid = pd.DataFrame(columns=['start', 'end', 'sum'])

    start_zone = close_max
    for index in range(0, int(close_delta / grid_step) +1):
        df_grid.loc[index, 'start'] = start_zone
        end_zone = start_zone - grid_step
        df_grid.loc[index, 'end'] = end_zone
        start_zone = end_zone

    df_grid['sum'] = 0
    for price in df_symbol['close'].to_list():
        index = get_zone_position(df_grid, price)
        df_grid.loc[index, 'sum'] = df_grid.loc[index, 'sum'] + 1

    df_symbol['close_zone'] = 0
    for index in range(0, len(df_symbol)):
        df_symbol['close_zone'][index] = get_zone_position(df_grid, df_symbol['close'][index])

    display = False
    if display:
        df_grid.to_csv('grid_' + symbol + '.csv')

        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(go.Bar(x=df_grid.index.tolist(), y=df_grid['sum'].tolist()),
                      row=1, col=1)
        # figure = px.bar(df_grid, y='sum', height=400, text='sum')
        # figure.show()


        fig.add_trace(go.Scatter(x=df_symbol.index.tolist(), y=df_symbol['close_zone'].tolist()),
                      row=2, col=1)
        # figure_2 = px.scatter(df_symbol, y='close_zone', height=800, text='close_zone')
        # figure_2.show()

        fig.update_layout(height=800, width=800, title_text="Side By Side Subplots")
        fig.show()

    return df_symbol, df_grid

def get_zone_position(df_grid, price):
    try:
        zone = df_grid[((df_grid['start'] > price) & ((df_grid['end']) <= price))].index[0]
    except:
        print('ZONE ERROR')
        if df_grid['start'][0] == price:
            zone = 0
        else:
            zone = -1
    return zone
