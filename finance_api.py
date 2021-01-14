from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import load_dotenv
import os

load_dotenv()
finance_key = os.getenv('FINANCE_API_KEY')

def get_daily(ticker_symbol):
    ts = TimeSeries(finance_key)
    stock_data, meta = ts.get_daily(symbol=ticker_symbol.upper())

    return stock_data

def get_quote_endpoint(ticker_symbol):
    ts = TimeSeries(finance_key)
    stock_data, meta = ts.get_quote_endpoint(symbol=ticker_symbol.upper())

    return stock_data

def get_intraday(ticker_symbol):
    ts = TimeSeries(finance_key)
    stock_data, meta = ts.get_daily(symbol=ticker_symbol.upper(), interval='5min', outputsize='full')

    return stock_data

def get_company_overview(ticker_symbol):
    fd = FundamentalData(finance_key)
    stock_data, meta = fd.get_company_overview(symbol=ticker_symbol.upper())

    return stock_data