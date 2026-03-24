# Research Report: Daily Options Quotes for GOOG & NFLX on Raspberry Pi 4

## Overview
This report identifies the most reliable and free way to fetch daily options quotes (Bid, Ask, and Last/Mark price) for specific target options on a Raspberry Pi 4. 

## Primary Recommendation: Yahoo Finance via `yfinance`
For a free, Python-friendly solution without expensive subscriptions, **Yahoo Finance** remains the most accessible source. The library `yfinance` is the industry standard for unofficial scraping, while `yahooquery` is a robust alternative.

### Target Symbols (Yahoo Finance Format)
Yahoo Finance uses a specific 21-character format for options: `TICKER` + `YYMMDD` + `C/P` + `STRIKE (8 digits)`.
*   **GOOG 2026-04-02 302.50 Call**: `GOOG260402C00302500`
*   **NFLX 2026-04-02 96.00 Call**: `NFLX260402C00096000`
    *   *Note: April 2, 2026, is a Thursday expiration due to the Good Friday market holiday on April 3.*

### Implementation Details (Python)
Both `yfinance` and `yahooquery` are fully compatible with the Raspberry Pi 4 (ARM64).

#### Using `yfinance`
```python
import yfinance as yf

def get_option_quote(ticker_symbol, expiry_date, strike_price):
    ticker = yf.Ticker(ticker_symbol)
    # Fetch the option chain for the specific date
    opt = ticker.option_chain(expiry_date)
    calls = opt.calls
    
    # Filter for the target strike
    target = calls[calls['strike'] == strike_price]
    
    if not target.empty:
        quote = target.iloc[0]
        bid = quote['bid']
        ask = quote['ask']
        last = quote['lastPrice']
        mark = (bid + ask) / 2  # Mark price calculation
        return {"bid": bid, "ask": ask, "last": last, "mark": mark}
    return None

# Example usage
# print(get_option_quote("GOOG", "2026-04-02", 302.50))
```

## Constraints and Considerations

### 1. Rate Limits
*   **Yahoo Finance**: Does not publish official rate limits for its unauthorized API. However, it is generally safe for personal use up to ~2,000 requests per hour per IP. 
*   **Raspberry Pi Strategy**: For a "daily tracker," a single request per ticker per hour (or even per day) is well within safe limits.

### 2. Mark Price Calculation
Yahoo Finance does not provide a "Mark Price" field directly. The standard industry practice is to calculate the **Midpoint** (average of Bid and Ask) to represent the Mark Price.

### 3. Raspberry Pi 4 (ARM64) Compatibility
*   **Library Installation**: Use `pip install yfinance pandas`. 
*   **Optimization**: Since the Pi 4 has limited resources compared to a server, avoid frequent polling. `pandas` can be slow to import; for a lightweight alternative, consider using `yahooquery` which has fewer dependencies or direct `requests` to the Yahoo Finance JSON endpoint if performance becomes an issue.

### 4. Alternative Sources (Comparison)
| Source | Cost | Python Support | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **Yahoo Finance** | Free | Excellent | No API key, easy setup | Unofficial, can break if site layout changes |
| **Tradier** | Free (with account) | Good | Official API, high reliability | Requires brokerage account sign-up |
| **Alpha Vantage** | Paid (Options) | Good | Official, structured | Options data is behind a premium paywall |

## Conclusion
The combination of `yfinance` and a simple midpoint calculation for the Mark Price is the best free, Python-friendly approach for this project. The symbols and dates provided are valid for the irregular expiration in April 2026.

**Recommended Action**: Install `yfinance` on the Pi 4 and use the `option_chain()` method to fetch the required DataFrames.
