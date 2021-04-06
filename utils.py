import pandas as pd
from collections import namedtuple
from typing import Tuple


def int_str_split(string) -> Tuple[int, str]:
    """
    splits string into integer and remaining string, e.g. 13D -> (13, 'D')
    """
    for i in range(len(string), -1, -1):
        if string[:i].isnumeric():
            return int(string[:i]), string[i:]
    return 1, string


def extract_close_prices_and_volumes(df: pd.DataFrame, args: namedtuple) -> (pd.Series, pd.Series):
    """
    Groups pandas DataFrame with given period and extracts the close prices and overall volume of that period
    :param df: DataFrame object of candles data
    :param args: namedtuple of arguments of start, end, grouping params
    :returns: tuple(close prices, volumes)
    """

    volumes = df.groupby(pd.Grouper(freq=args.period))["volume"].sum()
    start = pd.Timestamp(args.start) if args.start else volumes.index[0]
    end = pd.Timestamp(args.end) if args.end else volumes.index[-1]

    interval = volumes.loc[start: end].index

    dt_value, dt_unit = int_str_split(args.period)
    close_prices = df.reindex(
        interval + pd.Timedelta(dt_value, unit=dt_unit) - pd.Timedelta(minutes=1)
    )["close"]
    close_prices.index = interval

    return close_prices, volumes
