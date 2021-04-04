def rsi(close_prices, rsi_window):
    diff = close_prices.diff()
    gains, losses = diff.copy(), diff.copy()
    gains[gains < 0] = 0
    losses[losses > 0] = 0
    rs = gains.rolling(window=rsi_window).mean() / losses.rolling(window=rsi_window).mean().abs()
    return 100 - 100 / (1 + rs)