# portfolio_manager.py

import time
from constants import TICKERS
from game_state import alerts, time_indices, portfolio
from data_loader import prices_by_ticker
import game_state  # ✅ 전체를 import하여 순환 참조 방지


def buy_stock(ticker, quantity):
    index = min(game_state.time_indices[ticker], len(prices_by_ticker[f"{ticker}_Close"]) - 1)
    price = float(prices_by_ticker[f"{ticker}_Close"][index])
    total_cost = price * quantity

    if game_state.portfolio['cash'] >= total_cost:
        game_state.portfolio['cash'] -= total_cost
        info = game_state.portfolio['stocks'][ticker]
        total_qty = info['quantity']
        avg_price = info['buy_price']
        new_total_cost = total_qty * avg_price + total_cost
        new_total_qty = total_qty + quantity
        info['quantity'] = new_total_qty
        info['buy_price'] = new_total_cost / new_total_qty
        alerts.append((f"Bought {quantity} {ticker} @ ${price:.2f}", time.time()))  # ✅ 가격 포함 메시지
    else:
        max_qty = int(game_state.portfolio['cash'] // price)
        if max_qty >= 1:
            game_state.portfolio['cash'] -= price * max_qty
            info = game_state.portfolio['stocks'][ticker]
            total_qty = info['quantity']
            avg_price = info['buy_price']
            new_total_cost = total_qty * avg_price + price * max_qty
            new_total_qty = total_qty + max_qty
            info['quantity'] = new_total_qty
            info['buy_price'] = new_total_cost / new_total_qty
            alerts.append((f"Partially bought {max_qty} {ticker} @ ${price:.2f}", time.time()))  # ✅
        else:
            alerts.append((f"Not enough cash to buy {quantity} {ticker}", time.time()))


def sell_stock(ticker, quantity):
    info = game_state.portfolio['stocks'][ticker]
    if info['quantity'] == 0:
        alerts.append((f"No {ticker} to sell", time.time()))
        return

    index = min(game_state.time_indices[ticker], len(prices_by_ticker[f"{ticker}_Close"]) - 1)
    price = float(prices_by_ticker[f"{ticker}_Close"][index])
    sell_qty = min(quantity, info['quantity'])

    game_state.portfolio['cash'] += price * sell_qty
    info['quantity'] -= sell_qty
    if info['quantity'] == 0:
        info['buy_price'] = 0

    alerts.append((f"Sold {sell_qty} {ticker} @ ${price:.2f}", time.time()))  # ✅ 가격 포함 메시지


__all__ = ["buy_stock", "sell_stock", "portfolio"]
