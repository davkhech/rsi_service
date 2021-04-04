import argparse
import pandas as pd
import plotly.express as px

from rsi import rsi
from utils import extract_close_prices_and_volumes


def parse_args():
    parser = argparse.ArgumentParser("Calculate RSI for given candles")
    parser.add_argument('candles', 
                        type=str, help='path to candles json file')
    parser.add_argument('--period', '-p', 
                        type=str, default='D', 
                        help='candles period, can have values of pandas Grouper, e.g. 3H, D')
    parser.add_argument('--rsi_length', '-l', 
                        type=int, default=14, help='RSI window length')
    parser.add_argument('--start', '-s',
                        type=str, help='start of the period to calculate RSI for, e.g 2020-01-01')
    parser.add_argument('--end', '-e',
                        type=str, help='end of the period to calculate RSI for, e.g. 2020-01-01')
    parser.add_argument('--output', '-o',
                        type=str, default='rsi.csv', help='RSI output csv file path')
    parser.add_argument('--plot-trades', action='store_true', default=False, 
                        help='show barchart of trades vs hour of the day')
    return parser.parse_args()


def main(args):
    df = pd.read_json(args.candles, date_unit="ms").set_index("_id")
    df.index = pd.to_datetime(df.index, unit="ms")

    close_prices, volumes = extract_close_prices_and_volumes(df, args)

    rsi_df = rsi(close_prices, args.rsi_length)
    rsi_df.to_csv(args.output, header=['rsi'])

    print(f'The correlation between the volume and RSI is {volumes.corr(rsi_df):.4}')
    print(f'RSI is above 70 or below 30 in {((rsi_df > 70) | (rsi_df < 30)).mean() * 100:.4}% of times')

    if args.plot_trades:
        trades = df.groupby(df.index.hour)["number_of_trades"].sum()
        fig = px.bar(trades, labels={'_id': 'hrs', 'value': 'trades'})
        fig.show()

if __name__ == "__main__":
    main(parse_args())
