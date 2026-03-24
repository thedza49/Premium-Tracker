# Premium-Tracker (Covered Call Retention)

## Project Overview
This project tracks the daily performance of sold covered calls to monitor how much of the initial premium is "retained" leading up to expiration.

## Trades (Sold Short)
| Symbol | Expiration | Strike | Qty | Entry Price | Entry Date | Total Premium |
|--------|------------|--------|-----|-------------|------------|---------------|
| GOOG   | 2026-04-02 | 302.50 | 6   | $2.95       | 2026-03-24 | $1,770        |
| NFLX   | 2026-04-02 | 96.00  | 12  | $0.72       | 2026-03-24 | $864          |

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
