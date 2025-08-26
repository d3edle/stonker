import yfinance as yf
def get_current_price_sync(ticker: str):
    stock = yf.Ticker(ticker)
    todays_data = stock.history(period='1d')
    return todays_data['Close'][0]


