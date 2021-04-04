import argparse
import pandas as pd

from rsi import rsi


def parse_args():
    parser = argparse.ArgumentParser("Calculate RSI")
    parser.add_argument('candles', 
                        type=str, help='path to candles json file')
    parser.add_argument('--period', '-p', 
                        type=str, default='D', 
                        help='candles period, can have values of pandas grouper, e.g. 3H, D')
    parser.add_argument('--rsi_length', '-l', 
                        type=int, default=14, help='RSI window length')
    parser.add_argument('--start', '-s',
                        type=str, help='start of the period to calculate RSI for, e.g 2020-01-01')
    parser.add_argument('--end', '-e',
                        type=str, help='end of the period to calculate RSI for, e.g. 2020-01-01')
    parser.add_argument('--output', '-o',
                        type=str, default='rsi.csv', help='rsi output csv file path')
    return parser.parse_args()


def int_str_split(string):
    for i in range(len(string), -1, -1):
        if string[:i].isnumeric():
            return int(string[:i]), string[i:]
    return 1, string


def main(args):
    df = pd.read_json(args.candles, date_unit="ms").set_index("_id")
    df.index = pd.to_datetime(df.index, unit="ms")
    
    volumes = df.groupby(pd.Grouper(freq=args.period))["volume"].sum()
    start = pd.Timestamp(args.start) if args.start else volumes.index[0]
    end = pd.Timestamp(args.end) if args.end else volumes.index[-1]

    interval = volumes.loc[start: end].index

    dt_value, dt_unit = int_str_split(args.period)
    close_prices = df["close"][interval + pd.Timedelta(dt_value, unit=dt_unit) - pd.Timedelta(minutes=1)]
    close_prices.index = interval

    rsi_df = rsi(close_prices, args.rsi_length)
    rsi_df.to_csv(args.output, header=['rsi'])


if __name__ == "__main__":
    main(parse_args())