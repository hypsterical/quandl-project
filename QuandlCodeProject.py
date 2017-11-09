
import requests
import pandas as pd
import json
from StringIO import StringIO
import passwords.py
from collections import OrderedDict


def getMonthlyAverages(df, printToScreen = False):
    # groupby month and take averages
    period = df.date.dt.to_period("M")
    df_monthly = df.groupby(['ticker', period]).mean()
    df_monthly.reset_index(level='date', inplace=True)
    df_return = df_monthly[['adj_open', 'adj_close']]
    df_return['date'] = df_monthly['date'].apply(lambda x: x.strftime('%Y-%m'))
    df_return.rename(columns={'date': 'month', 'adj_open': 'average_open', 'adj_close': 'average_close'}, inplace=True)
    df_return = df_return[['month', 'average_open', 'average_close']]

    if(printToScreen):
        # format values in json and pretty print to command line
        formatted = df_return.groupby(level=0).apply(lambda x: x.to_json(orient='records', force_ascii=True)).to_json()
        s_formatted = formatted.decode('unicode-escape')
        s_formatted = s_formatted.replace('\"[', '[')
        s_formatted = s_formatted.replace(']\"', ']')
        json_formatted = json.loads(s_formatted, object_pairs_hook=OrderedDict)
        print json.dumps(json_formatted, indent=4, separators=(',', ': '), sort_keys=False)
    return df_return

def getBiggestLoser(df, printToScreen = False):

    return True

def maxProfitDay(df, printToScreen = False):
    #calculate day with max profit for each stock, and return rows
    df['day_change']= df['close'] - df['open']
    idx = df.groupby(level=0)['day_change'].transform(max) == df['day_change']
    if(printToScreen):
        print df[idx]
    return df[idx]

if __name__ == "__main__":
    #get program args
    tickers = 'AAPL,GOOG'
    start_date = '2017-04-01'
    end_date = '2017-10-31'
    publisher = 'WIKI'
    table = 'PRICES'
    #pull api key from file
    api_key = passwords.QUANDL_API_KEY

    #format https://www.quandl.com/api/v3/datatables/{publisher}/{table}/metadata
    request_string = "https://www.quandl.com/api/v3/datatables/{}/{}.csv?date.gte={}&date.lte={}&ticker={}&api_key={}".format(publisher, table, start_date, end_date,tickers, api_key)
    r = requests.get(request_string)
    df = pd.DataFrame.from_csv(StringIO(r.content), index_col='ticker')
    df['date'] = pd.to_datetime(df['date'])
    getMonthlyAverages(df, True)


