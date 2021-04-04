import pandas as pd


def rsi(close_prices: pd.Series, rsi_window: int = 14) -> pd.Series:
    """
    Calculates RSI index for given close times
    :param close_prices: pd.Series of candle close prices
    :param rsi_window: RSI window length, default is 14
    :returns: pd.Series of RSI values
    """
    diff = close_prices.diff()
    gains, losses = diff.copy(), diff.copy()
    gains[gains < 0] = 0
    losses[losses > 0] = 0
    rs = gains.rolling(window=rsi_window).mean() / losses.rolling(window=rsi_window).mean().abs()

    return 100 - 100 / (1 + rs)
