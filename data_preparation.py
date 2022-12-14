import pandas as pd
import os
import config
import utils

default_features = ["open", "close", "high", "low", "volume"]


class DataDescription():
    def __init__(self, lst_symbols, lst_features):
        self.symbols = lst_symbols
        self.features = lst_features


def get_current_data(data_description):
    symbols = ','.join(data_description.symbols)
    symbols = symbols.replace('/', '_')
    params = {"service": "history", "exchange": "ftx", "symbol": symbols, "start": "2019-01-01", "interval": "1h"}
    response_json = utils.fdp_request(params)

    data = {feature: [] for feature in data_description.features}
    data["symbol"] = []

    if response_json["status"] == "ok":
        for symbol in data_description.symbols:
            formatted_symbol = symbol.replace('/', '_')
            df = pd.read_json(response_json["result"][formatted_symbol]["info"])
            # df = features.add_features(df, data_description.features)
            columns = list(df.columns)

            data["symbol"].append(symbol)
            for feature in data_description.features:
                if feature not in columns:
                    return None
                data[feature].append(df[feature].iloc[-1])

    df_result = pd.DataFrame(data)
    df_result.set_index("symbol", inplace=True)
    return df_result


def record(symbol, start_date="2022-06-01", interval="1h"):
    symbol = symbol.replace('/','_')
    params = { "service":"history", "exchange":"ftx", "symbol":symbol, "start":start_date, "interval": interval }
    response_json = utils.fdp_request(params)

    formatted_symbol = symbol.replace('/','_')
    if response_json["result"][formatted_symbol]["status"] == "ko":
        print("no data for ",symbol)

    df = pd.read_json(response_json["result"][formatted_symbol]["info"])
    # df = features.add_features(df, data_description.features)
    df2 = pd.DataFrame()

    df2['close'] = df['close'].copy()

    return df2