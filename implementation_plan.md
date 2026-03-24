# Implementation Plan: Premium-Tracker

This plan outlines the steps for Momo to implement a daily tracker for Daniel's sold covered calls on his Raspberry Pi 4.

## 1. Overview
The "Premium-Tracker" will fetch daily options quotes for specific symbols using `yfinance`, calculate key performance metrics (Mark Price, Premium Retention %, and Unrealized P/L), and store the results in a historical JSON file. It will also produce a summary for Telegram notifications.

## 2. Technical Specs
- **Target Symbols (from `trades.json`):**
    - `GOOG260402C00302500` (GOOG 2026-04-02 302.50 Call)
    - `NFLX260402C00096000` (NFLX 2026-04-02 96.00 Call)
- **Data Storage:** `premium-tracker/daily_stats.json`
- **Dependency:** `yfinance`, `pandas` (for yfinance)

## 3. Logic & Formulas
- **Mark Price:** `(Bid + Ask) / 2`
- **Premium Retention %:** `(1 - (Mark Price / Entry Price)) * 100`
- **Unrealized P/L:** `(Entry Price - Mark Price) * Quantity * 100`
- **Daily Snapshot:** A record containing the date, per-trade metrics, and the aggregate total unrealized P/L.

## 4. Implementation Tasks (TDD-focused)

### Task 1: Data Models & Trade Loading
**Goal:** Define the data structure and load existing trades from `trades.json`.
- Create `premium-tracker/main.py`.
- Define a `Trade` data class/model.
- Implement a function to load trades from `trades.json`.
- **Test:** Verify that `trades.json` is correctly parsed into `Trade` objects.

### Task 2: Quote Fetching & Calculation Logic
**Goal:** Implement the logic to fetch live data and calculate metrics.
- Implement a function `fetch_mark_price(symbol)` using `yfinance` (mocking the API call for tests).
- Implement a calculation engine that takes a `Trade` and a `Mark Price` to produce:
    - `mark_price`
    - `retention_pct`
    - `unrealized_pl`
- **Test:** Verify calculations with known inputs (e.g., Entry 2.95, Mark 2.50, Qty 6).

### Task 3: Persistence & Historical Snapshots
**Goal:** Save the daily results to `daily_stats.json`.
- Implement logic to create a daily snapshot record.
- Append the snapshot to `premium-tracker/daily_stats.json`.
- Ensure the script handles the file creation if it doesn't exist and avoids duplicate entries if run multiple times on the same day.
- **Test:** Verify that calling the save function appends a valid JSON record to the file.

### Task 4: Summary Output for Telegram
**Goal:** Generate a human-readable summary for Nia to send to Daniel.
- Create a function to format the daily stats into a clean string.
- Example format:
  ```
  📈 Premium Retention Report - 2026-03-24
  
  GOOG: $2.50 Mark | 15.2% Retained | +$270.00 P/L
  NFLX: $0.60 Mark | 16.7% Retained | +$144.00 P/L
  
  Total Unrealized P/L: +$414.00
  ```
- **Test:** Verify the output string format matches the requirement.

## 5. Automation Plan
- **Cron Job:** The script will be scheduled via `cron` on the Raspberry Pi 4.
- **Schedule:** Suggested run at 1:15 PM PT (market close) or nightly.
- **Command:** `python3 /home/daniel/.openclaw/workspace/premium-tracker/main.py`
- **Action:** Nia will be responsible for setting up the cron job once Larry approves the implementation.

## 6. Project Structure
- `premium-tracker/main.py` (Entry point)
- `premium-tracker/trades.json` (Input - Config)
- `premium-tracker/daily_stats.json` (Output - Database)
- `premium-tracker/test_main.py` (Tests)
