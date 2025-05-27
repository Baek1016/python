# 📁 trade_logger.py

import csv
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "trade_log.csv")

def log_trade(action, ticker, quantity, price, fee, cash):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    is_new = not os.path.exists(LOG_FILE)
    
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["datetime", "action", "ticker", "quantity", "price", "fee", "remaining_cash"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            action,
            ticker,
            quantity,
            round(price, 2),
            round(fee, 2),
            round(cash, 2)
        ])
