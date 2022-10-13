import pandas as pd

FDP_URL='https://fdp-ifxcxetwza-uc.a.run.app/'

lst_intervals = ['1h', '1d']

lst_default_symbols = [
        "BTC/USD",
        "ETH/USD",
        "DOGE/USD",
        "MANA/USD",
        "CHZ/USD",
        "AAVE/USD",
        "BNB/USD",
        "MATIC/USD",
        "XRP/USD",
        "SAND/USD",
        "OMG/USD",
        "CRV/USD",
        "TRX/USD",
        "FTT/USD",
        "GRT/USD",
        "SRM/USD",
        "FTM/USD",
        "LTC/USD",
        "RUNE/USD",
        "CRO/USD",
        "UNI/USD",
        "SUSHI/USD",
        "LRC/USD",
        "LINK/USD",
        "BCH/USD",
        "AXS/USD",
        "RAY/USD",
        "SOL/USD",
        "AVAX/USD"
    ]

lst_default_step = [0.5, 1, 2, 3, 4, 5]

init_date_string = "2022-06-01"
init_symbol = lst_default_symbols[0]
init_step_percent = lst_default_step[1]
init_interval = lst_intervals[0]

df_symbol = pd.DataFrame()
df_grid = pd.DataFrame()
