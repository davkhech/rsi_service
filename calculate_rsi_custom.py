import pandas as pd
import matplotlib.pyplot as plt

from calculate_rsi import parse_args
from utils import extract_close_prices_and_volumes


class RSI:
    def __init__(self, window_size=14):
        self.last_price = None
        self.gain = 0
        self.loss = 0
        self.window = window_size
        self.n = -1
        
    def feed(self, price):
        self.n += 1
        if self.n == 0:
            self.last_price = price
            return None
        
        if self.n <= self.window:
            self.gain += (price - self.last_price) / self.window if price - self.last_price > 0 else 0
            self.loss += (self.last_price - price) / self.window if self.last_price - price > 0 else 0
            return None
        
        self.gain = ((self.window - 1) * self.gain + 
                     (price - self.last_price if price - self.last_price > 0 else 0)
                    ) / self.window
        self.loss = ((self.window - 1) * self.loss + 
                     (self.last_price - price if self.last_price - price > 0 else 0)
                    ) / self.window

        self.last_price = price
        rs = self.gain / self.loss
        return 100 - 100 / (1 + rs)


def main(args):
    df = pd.read_json(args.candles, date_unit="ms").set_index("_id")
    df.index = pd.to_datetime(df.index, unit="ms")

    close_prices, volumes = extract_close_prices_and_volumes(df, args)
    rsi = RSI(args.rsi_length)

    rsi_v = []
    for cp in close_prices:
        rsi_v.append(rsi.feed(cp))

    rsi_df = pd.Series(rsi_v)
    rsi_df.index = close_prices.index

    print(f'The correlation between the volume and RSI is {volumes.corr(rsi_df):.4}')
    print(f'RSI is above 70 or below 30 in {((rsi_df > 70) | (rsi_df < 30)).mean() * 100:.4}% of times')


if __name__ == "__main__":
    main(parse_args())
