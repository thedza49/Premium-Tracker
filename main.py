# Premium-Tracker script for Daniel
# Built by Momo (Builder)
# Requirements: Python 3, yfinance, pandas, json, datetime
# Note: Using yahooquery as primary data source due to yfinance connectivity issues (fc.yahoo.com blocked/unreachable).

import json
import datetime
import os
import sys
import pandas as pd # Required by specs
try:
    import yfinance as yf # Required by specs
except ImportError:
    pass

from yahooquery import Ticker

# Constants
TRADES_FILE = "premium-tracker/trades.json"
EVENTS_FILE = "premium-tracker/company_events.json"
STATS_FILE = "premium-tracker/daily_stats.json"

def load_trades():
    with open(TRADES_FILE, 'r') as f:
        return json.load(f)["trades"]

def load_events():
    with open(EVENTS_FILE, 'r') as f:
        return json.load(f)

def format_occ_symbol(trade):
    # expiration is YYYY-MM-DD
    exp_date = datetime.datetime.strptime(trade["expiration"], "%Y-%m-%d")
    exp_formatted = exp_date.strftime("%y%m%d")
    strike_formatted = f"{int(trade['strike'] * 1000):08d}"
    return f"{trade['symbol']}{exp_formatted}{trade['type']}{strike_formatted}"

def get_option_metrics(occ_symbol, entry_price, quantity):
    try:
        t = Ticker(occ_symbol)
        sd = t.summary_detail.get(occ_symbol, {})
        
        bid = sd.get('bid')
        ask = sd.get('ask')
        
        if bid is None or ask is None:
            # Fallback to regularMarketPrice if bid/ask missing
            mark_price = sd.get('regularMarketPrice')
            if mark_price is None:
                # Fallback to price
                price_data = t.price.get(occ_symbol, {})
                mark_price = price_data.get('regularMarketPrice')
            
            if mark_price is None:
                return None
        else:
            mark_price = (bid + ask) / 2
        
        retention_pct = (1 - (mark_price / entry_price)) * 100
        unrealized_pl = (entry_price - mark_price) * quantity * 100
        
        return {
            "mark_price": mark_price,
            "retention_pct": retention_pct,
            "unrealized_pl": unrealized_pl
        }
    except Exception as e:
        print(f"Error fetching data for {occ_symbol}: {e}", file=sys.stderr)
        return None

def check_events(events):
    today = datetime.date.today().strftime("%Y-%m-%d")
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    found_events = []
    for event in events:
        if event["date"] in [today, tomorrow]:
            prefix = "TODAY" if event["date"] == today else "TOMORROW"
            found_events.append(f"[{prefix}] {event['company']}: {event['event_type']} - {event['description']}")
    
    return found_events

def main():
    trades = load_trades()
    events = load_events()
    
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    trade_stats = []
    total_keep = 0.0
    total_original = 0.0
    
    summary_lines = [f"📊 Covered Call Premium Report - {today_str}", ""]
    
    for trade in trades:
        occ_symbol = format_occ_symbol(trade)
        metrics = get_option_metrics(occ_symbol, trade["entry_price"], trade["quantity"])
        
        if metrics:
            trade_stats.append({
                "symbol": trade["symbol"],
                "occ_symbol": occ_symbol,
                "metrics": metrics
            })
            
            original_premium = trade['entry_price'] * trade['quantity'] * 100
            cost_to_close = metrics['mark_price'] * trade['quantity'] * 100
            amount_keep = original_premium - cost_to_close
            
            total_original += original_premium
            total_keep += amount_keep
            
            summary_lines.append(f"**{trade['symbol']} (${trade['strike']} Call):**")
            summary_lines.append(f"🔹 **Original Premium:** ${original_premium:,.2f} (Already in your pocket)")
            summary_lines.append(f"🔹 **Cost to Close Now:** ${cost_to_close:,.2f} (If you bought the contracts back today)")
            summary_lines.append(f"🔹 **Amount You Keep:** **${amount_keep:,.2f}** (Total profit if you exit now)")
            summary_lines.append(f"🔹 **Premium Retained:** {metrics['retention_pct']:.1f}%")
            summary_lines.append("")
        else:
            summary_lines.append(f"{trade['symbol']}: Data unavailable.")
    
    summary_lines.append(f"**Total Profit if You Exit Now: ${total_keep:,.2f}**")
    if total_original > 0:
        summary_lines.append(f"*(Total original premium was ${total_original:,.2f}. You're holding on to {(total_keep/total_original)*100:.1f}% of it today.)*")
    
    # Check for events
    upcoming_events = check_events(events)
    if upcoming_events:
        summary_lines.append("")
        summary_lines.append("🗓️ Upcoming Company Events:")
        summary_lines.extend(upcoming_events)
    
    final_summary = "\n".join(summary_lines)
    
    # Save to stats file
    daily_snapshot = {
        "date": today_str,
        "total_keep": total_keep,
        "trades": trade_stats
    }
    
    all_stats = []
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            try:
                all_stats = json.load(f)
            except json.JSONDecodeError:
                all_stats = []
    
    # Update or append
    updated = False
    for i, snapshot in enumerate(all_stats):
        if snapshot["date"] == today_str:
            all_stats[i] = daily_snapshot
            updated = True
            break
    
    if not updated:
        all_stats.append(daily_snapshot)
    
    with open(STATS_FILE, 'w') as f:
        json.dump(all_stats, f, indent=2)
    
    # Final output to stdout
    print(final_summary)

if __name__ == "__main__":
    main()
