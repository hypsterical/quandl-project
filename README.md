# quandl-project

To run the project, first populate passwords-TEMPLATE.py with your Quandl API-Key:
QUANDL_API_KEY = YOUR_API_KEY_HERE
Then, rename passwords-TEMPLATE to passwords.py.

Next, run QuandlCodeProject at the command line with the following parameters:
STOCK_TICKERS, START_DATE, END_DATE
STOCK_TICKERS = comma delimited string of tickers to analyze
START_DATE = starting date for data in the format of YYYY-MM-DD
END_DATE = ending date for data in the format of YYYY-MM-DD

example program command line run:
python QuandleCodeProject.py "AAPL,GOOG" "2017-01-01" "2017-04-30"

Optional Parameters:
--max-daily-profit
Day for each stock that would have yielded the largest profit
--busy-day
Busiest day for each stock by volume
--biggest-loser
Stock with the most number of days with a close price lower than open