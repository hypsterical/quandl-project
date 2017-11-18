# quandl-project
Simple project demonstrating quandl api calls and data manipulation in python.

## Dependencies:
 Python 2.7
 Libraries: Numpy, Pandas, Requests

## Running the project
1. Populate passwords-TEMPLATE.py with your [Quandl](https://www.quandl.com/) API-Key:
`QUANDL_API_KEY = YOUR_API_KEY_HERE`
Then, rename passwords-TEMPLATE to passwords.py.

2. Next, run QuandlCodeProject at the command line with the following parameters:
STOCK_TICKERS, START_DATE, END_DATE
STOCK_TICKERS = comma delimited string of tickers to analyze
START_DATE = starting date for data in the format of YYYY-MM-DD
END_DATE = ending date for data in the format of YYYY-MM-DD

example program command line run:
`python QuandleCodeProject.py "AAPL,GOOG" "2017-01-01" "2017-04-30"`

3. Optional Parameters:
--max-daily-profit
Day for each stock that would have yielded the largest profit
--busy-day
Busiest day for each stock by volume
--biggest-loser
Stock with the most number of days with a close price lower than open

Example program run with optional parameters
`python QuandleCodeProject.py "AAPL,GOOG" "2017-01-01" "2017-04-30" --biggest-loser --busy-day`
