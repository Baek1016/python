# 📁 portfolio_manager.py

import time
from constants import TICKERS
from data_loader import prices_by_ticker
import game_state  # ✅ 순환참조 방지
from trade_logger import log_trade  # ✅ 거래 로그 기록

FEE_RATE = 0.003  # ✅ 수수료율 (0.3%)

def buy_stock(ticker, quantity):
    index = min(game_state.time_indices[ticker], len(prices_by_ticker[f"{ticker}_Close"]) - 1)
    price = float(prices_by_ticker[f"{ticker}_Close"][index])
    fee = price * quantity * FEE_RATE
    total_cost = price * quantity + fee

    if game_state.portfolio['cash'] >= total_cost:
        game_state.portfolio['cash'] -= total_cost
        info = game_state.portfolio['stocks'][ticker]
        prev_qty = info['quantity']
        prev_price = info['buy_price']

        new_total_cost = prev_qty * prev_price + price * quantity
        new_total_qty = prev_qty + quantity
        info['quantity'] = new_total_qty
        info['buy_price'] = new_total_cost / new_total_qty

        game_state.alerts.append((f"Bought {quantity} {ticker} @ ${price:.2f} (Fee: ${fee:.2f})", time.time()))
        log_trade("BUY", ticker, quantity, price, fee, game_state.portfolio['cash'])
    else:
        max_qty = int(game_state.portfolio['cash'] // (price + price * FEE_RATE))
        if max_qty >= 1:
            fee = price * max_qty * FEE_RATE
            total_cost = price * max_qty + fee
            game_state.portfolio['cash'] -= total_cost

            info = game_state.portfolio['stocks'][ticker]
            prev_qty = info['quantity']
            prev_price = info['buy_price']
            new_total_cost = prev_qty * prev_price + price * max_qty
            new_total_qty = prev_qty + max_qty
            info['quantity'] = new_total_qty
            info['buy_price'] = new_total_cost / new_total_qty

            game_state.alerts.append((f"Partially bought {max_qty} {ticker} @ ${price:.2f} (Fee: ${fee:.2f})", time.time()))
            log_trade("BUY", ticker, max_qty, price, fee, game_state.portfolio['cash'])
        else:
            game_state.alerts.append((f"Not enough cash to buy {quantity} {ticker}", time.time()))

def sell_stock(ticker, quantity):
    info = game_state.portfolio['stocks'][ticker]
    if info['quantity'] == 0:
        game_state.alerts.append((f"No {ticker} to sell", time.time()))
        return

    index = min(game_state.time_indices[ticker], len(prices_by_ticker[f"{ticker}_Close"]) - 1)
    price = float(prices_by_ticker[f"{ticker}_Close"][index])
    sell_qty = min(quantity, info['quantity'])
    gross_income = price * sell_qty
    fee = gross_income * FEE_RATE
    net_income = gross_income - fee

    game_state.portfolio['cash'] += net_income
    info['quantity'] -= sell_qty
    if info['quantity'] == 0:
        info['buy_price'] = 0.0

    game_state.alerts.append((f"Sold {sell_qty} {ticker} @ ${price:.2f} (Fee: ${fee:.2f})", time.time()))
    log_trade("SELL", ticker, sell_qty, price, fee, game_state.portfolio['cash'])

# ✅ 모듈 외부에서 불러올 수 있도록 정의
__all__ = ["buy_stock", "sell_stock"]
