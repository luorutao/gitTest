import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_stock_price(symbol):
    """Get current stock price using yfinance"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        return current_price
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        return None

def get_stock_history(symbol, period="1mo"):
    """Get stock price history"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        print(f"Error getting history for {symbol}: {e}")
        return None

def get_recent_ipos():
    """
    Get recent IPOs - this is a simplified example
    In practice, you might want to use a dedicated IPO API
    """
    # Some example recent IPO symbols (you'd need to update these regularly)
    recent_ipos = [
        "PLTR",  # Palantir
        "SNOW",  # Snowflake
        "DASH",  # DoorDash
        "ABNB",  # Airbnb
        "RBLX",  # Roblox
    ]
    
    ipo_data = []
    for symbol in recent_ipos:
        price = get_stock_price(symbol)
        if price:
            stock = yf.Ticker(symbol)
            info = stock.info
            company_name = info.get('longName', 'N/A')
            market_cap = info.get('marketCap', 'N/A')
            
            ipo_data.append({
                'Symbol': symbol,
                'Company': company_name,
                'Current Price': price,
                'Market Cap': market_cap
            })
    
    return pd.DataFrame(ipo_data)

def main():
    print("=== Stock Price Checker ===")
    
    # Example: Get specific stock prices
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    print("\n--- Popular Stock Prices ---")
    for symbol in symbols:
        price = get_stock_price(symbol)
        if price:
            print(f"{symbol}: ${price:.2f}")
    
    # Get recent IPO data
    print("\n--- Recent IPO Stocks ---")
    ipo_df = get_recent_ipos()
    if not ipo_df.empty:
        print(ipo_df.to_string(index=False))
    
    # Example: Get stock history for a specific stock
    print("\n--- AAPL Recent History (Last 5 days) ---")
    hist = get_stock_history("AAPL", period="5d")
    if hist is not None and not hist.empty:
        print(hist[['Open', 'High', 'Low', 'Close', 'Volume']].round(2))

if __name__ == "__main__":
    main()
