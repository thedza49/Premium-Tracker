# Premium-Tracker (Covered Call Retention)

## Project Overview
This project tracks the daily performance of sold covered calls to monitor how much of the initial premium is "retained" leading up to expiration.

## Trades (Sold Short Example)
| Symbol | Expiration | Strike | Qty | Entry Price | Entry Date | Total Premium |
|--------|------------|--------|-----|-------------|------------|---------------|
| TICKER | 2026-04-02 | 100.00 | 10  | $1.00       | 2026-03-24 | $1,000        |

## Metrics to Track (Daily)
- **Current Mark:** Mid-price (between Bid and Ask) of the option.
- **Unrealized P/L:** (Entry Price - Current Mark) * Quantity * 100.
- **Premium Retention %:** (1 - (Current Mark / Entry Price)) * 100.
- **Days to Expiry (DTE):** Time left until expiration.

## Template Usage (Future Projects)
To reuse this for a new batch of covered calls:
1. Update `trades.json` with the new tickers, strikes, expirations, and entry prices.
2. Run `main.py` to start the new daily tracking cycle.
3. The script handles data fetching and reporting dynamically based on whatever is in `trades.json`.
