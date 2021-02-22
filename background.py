from database import sessionLocal
from models import Stock
import yfinance as yf

def fetch_stock_data(id: int):
    db = sessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()
    yahoo_data = yf.Ticker(stock.symbol)
    stock.ma200 = yahoo_data.info["twoHundredDayAverage"]
    stock.ma50 = yahoo_data.info["fiftyDayAverage"]
    stock.price = yahoo_data.info["previousClose"]
    stock.forward_pe = yahoo_data.info["forwardPE"]
    if yahoo_data.info["dividendYield"]:
        stock.dividend_yield = yahoo_data.info["dividendYield"] * 100
    


    db.add(stock)
    db.commit()
