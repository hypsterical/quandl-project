
import requests
import pandas as pd
import json
from StringIO import StringIO
import passwords
from collections import OrderedDict
import sys
import argparse
import numpy as np

def getMonthlyAverages(df, printToScreen = False):
    # groupby month and take averages
    period = df.date.dt.to_period("M")
    df_monthly = df.groupby([df.index, period]).mean()
    df_monthly.reset_index(level='date', inplace=True)
    df_monthly = df_monthly[['date', 'adj_open', 'adj_close']]
    df_monthly['date'] = df_monthly['date'].apply(lambda x: x.strftime('%Y-%m'))
    df_monthly.rename(columns={'date': 'month', 'adj_open': 'average_open', 'adj_close': 'average_close'}, inplace=True)
    df_monthly = df_monthly[['month', 'average_open', 'average_close']]

    if(printToScreen):
        # format values in json and pretty print to command line
        formatted = df_monthly.groupby(level=0).apply(lambda x: x.to_json(orient='records', force_ascii=True)).to_json()
        s_formatted = formatted.decode('unicode-escape')
        s_formatted = s_formatted.replace('\"[', '[')
        s_formatted = s_formatted.replace(']\"', ']')
        json_formatted = json.loads(s_formatted, object_pairs_hook=OrderedDict)
        #print "Monthly Averages for each stock: "
        print "Monthly Averages for each stock: "
        print json.dumps(json_formatted, indent=4, separators=(',', ': '), sort_keys=False)
        print ""
    return df_monthly

def getBiggestLoser(df, printToScreen = False):
    df['day_change'] = df['close'] - df['open']
    df['loser'] = np.where((df['day_change']) < 0, -1, 0)
    df_sum = df.groupby(level=0)['loser'].transform(sum)
    if(printToScreen):
        print "Biggest Loser: Stock with most number of days with a closing price less than open: "
        print "Ticker: " + str(df_sum.idxmin())
        print "Losing Days: " + str(np.abs(df_sum.min()))
        print ""
    return df_sum

def getMaxProfitDay(df, printToScreen = False):
    #calculate day with max profit for each stock, and return rows
    df['day_change']= df['close'] - df['open']
    idx = df.groupby(level=0)['day_change'].transform(max) == df['day_change']
    if(printToScreen):

        df_print = df[idx][['date', 'day_change']]
        df_print.rename(columns={'day_change': 'profit'}, inplace=True)
        print "Max Daily Profit in Date Range for each stock:"
        print df_print
        print ""

    return df[idx]

def getBusyDays(df, printToScreen = False):

    avg_vol = df.groupby(level=0)['volume'].transform(np.mean)
    df['avg_volume'] = avg_vol
    idx = df['avg_volume'] * 1.1 < df['volume']
    df_print = df[['date', 'volume', 'avg_volume']]

    if (printToScreen):
        print "Busy Days for Each Ticker (vol > mean_vol * 1.1): "
        for idx, item in df_print[idx].groupby(level=0):
            print "Ticker : " + str(idx)
            print "Average Volume: " + str(item["avg_volume"][0])
            print item[["date", 'volume']].to_string(index=False)
            print ""
    return df[idx]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tickers")
    parser.add_argument("date_start")
    parser.add_argument("date_end")
    parser.add_argument('--biggest-loser', action='store_true')
    parser.add_argument('--busy-day', action='store_true')
    parser.add_argument('--max-daily-profit', action='store_true')
    args = parser.parse_args()

    #get program args

    start_date = args.date_start
    tickers = args.tickers
    end_date = args.date_end
    publisher = 'WIKI'
    table = 'PRICES'
    #pull api key from file
    api_key = passwords.QUANDL_API_KEY

    #format https://www.quandl.com/api/v3/datatables/{publisher}/{table}/metadata
    request_string = "https://www.quandl.com/api/v3/datatables/{}/{}.csv?date.gte={}&date.lte={}&ticker={}&api_key={}".format(publisher, table, start_date, end_date,tickers, api_key)
    r = requests.get(request_string)
    df = pd.DataFrame.from_csv(StringIO(r.content), index_col='ticker')
    #if the dataframe is empty, there was an error in retrieving the data
    if (df.empty):
        print "ERROR retrieving data. Aborting..."
        sys.exit()

    df['date'] = pd.to_datetime(df['date'])
    getMonthlyAverages(df, True)

    if(args.biggest_loser):
        getBiggestLoser(df,True)
    if(args.busy_day):
        getBusyDays(df, True)
    if(args.max_daily_profit):
        getMaxProfitDay(df,True)



