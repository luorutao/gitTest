import requests
import pandas as pd
from datetime import datetime
import yfinance as yf

def get_nasdaq_upcoming_ipos():
    """
    Get upcoming IPOs from NASDAQ (this is a simplified example)
    Note: Real-world usage might need API keys or more sophisticated scraping
    """
    try:
        # This is a placeholder - you'd need to adapt based on the actual API/website
        # Many financial data providers offer IPO APIs (like Alpha Vantage, IEX Cloud, etc.)
        
        # For demonstration, let's create some mock upcoming IPO data
        upcoming_ipos = [
            {
                'Company': 'Example Corp A',
                'Symbol': 'EXPA',
                'Expected Date': '2025-08-15',
                'Price Range': '$15-18',
                'Shares': '10M'
            },
            {
                'Company': 'Tech Startup B',
                'Symbol': 'TSUB',
                'Expected Date': '2025-08-22',
                'Price Range': '$20-25',
                'Shares': '8M'
            }
        ]
        
        return pd.DataFrame(upcoming_ipos)
    
    except Exception as e:
        print(f"Error fetching upcoming IPOs: {e}")
        return pd.DataFrame()

def get_ipo_performance(symbol, ipo_date=None):
    """
    Analyze IPO performance - compare current price to IPO price
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Get historical data since IPO (if date provided) or max available
        if ipo_date:
            hist = stock.history(start=ipo_date)
        else:
            hist = stock.history(period="max")
        
        if hist.empty:
            return None
        
        ipo_price = hist['Open'].iloc[0]  # First day opening price
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        
        if current_price and ipo_price:
            performance = ((current_price - ipo_price) / ipo_price) * 100
            
            return {
                'Symbol': symbol,
                'Company': info.get('longName', 'N/A'),
                'IPO Price': round(ipo_price, 2),
                'Current Price': round(current_price, 2),
                'Performance (%)': round(performance, 2),
                'Days Since IPO': len(hist)
            }
    
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
        return None

def get_financial_data_sources():
    """
    Information about APIs and services for IPO data
    """
    sources = {
        'Free APIs': [
            'yfinance - Yahoo Finance data',
            'Alpha Vantage - Free tier available',
            'IEX Cloud - Free tier available',
            'Finnhub - Free tier available'
        ],
        'Paid Services': [
            'Bloomberg API',
            'Refinitiv (Reuters)',
            'Quandl',
            'Polygon.io'
        ],
        'Web Sources': [
            'SEC EDGAR filings',
            'NASDAQ IPO calendar',
            'NYSE IPO calendar',
            'IPO Scoop',
            'Renaissance Capital IPO ETF'
        ]
    }
    
    return sources

def main():
    print("=== IPO Stock Analysis Tool ===")
    
    # Show upcoming IPOs (mock data)
    print("\n--- Upcoming IPOs ---")
    upcoming = get_nasdaq_upcoming_ipos()
    if not upcoming.empty:
        print(upcoming.to_string(index=False))
    
    # Analyze some known IPO stocks performance
    print("\n--- Recent IPO Performance Analysis ---")
    ipo_stocks = [
        ('SNOW', '2020-09-16'),  # Snowflake
        ('PLTR', '2020-09-30'),  # Palantir
        ('RBLX', '2021-03-10'),  # Roblox
    ]
    
    performance_data = []
    for symbol, ipo_date in ipo_stocks:
        perf = get_ipo_performance(symbol, ipo_date)
        if perf:
            performance_data.append(perf)
    
    if performance_data:
        perf_df = pd.DataFrame(performance_data)
        print(perf_df.to_string(index=False))
    
    # Show data sources information
    print("\n--- Financial Data Sources ---")
    sources = get_financial_data_sources()
    for category, source_list in sources.items():
        print(f"\n{category}:")
        for source in source_list:
            print(f"  • {source}")

if __name__ == "__main__":
    main()
