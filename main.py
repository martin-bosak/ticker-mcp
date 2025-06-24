from fastmcp import FastMCP
import yfinance as yf
import datetime

mcp = FastMCP("Ticker MCP Server", log_level="DEBUG")

@mcp.tool()
def yfinance_search(query: str):
    """
    Search for a stock on yfinance
    Args:
        query: str - the query to search for
    Returns:
        json
    """
    print(f"Searching for {query} on yfinance")
    result = yf.Search(query)
    return result.all


@mcp.tool()
def get_stock_data(ticker: str, period_days: int = 30):
    """
    Get historical data for a stock
    Args:
        ticker: str - the ticker on yfinance
        period_days: int - the number of days to get the data for, default is 30 days
    Returns:
        json
    """
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=period_days)
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
    
    result = []
    ath_sf = 0  # Initialize all-time high
    atl_sf = float('inf')  # Initialize all-time low
    
    for index, row in stock_data.iterrows():
        r = row.to_dict()
        r['Date'] = index
        if r.get('High', 0) > 0:
            if r.get('High', 0) > ath_sf:
                ath_sf = r['High']
            r['ATH'] = ath_sf
            if r.get('Low', float('inf')) < atl_sf:
                atl_sf = r['Low']
            r['ATL'] = atl_sf
            r['PCT_ATH'] = (r['High']) / r['ATH']
            r['PCT_ATL'] = (r['Low']) / r['ATL']
        result.append(r)

    return result



if __name__ == "__main__":
    mcp.run()