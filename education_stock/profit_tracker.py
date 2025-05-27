# ✅ profit_tracker.py
import matplotlib.pyplot as plt
import os

def plot_profit_history(profit_list, save_path="logs/profit_chart.png"):
    if not profit_list:
        return

    if not os.path.exists("logs"):
        os.makedirs("logs")

    plt.figure(figsize=(10, 4))
    plt.plot(profit_list, label="Total Profit", color="lime")
    plt.xlabel("Day")
    plt.ylabel("Profit ($)")
    plt.title("Profit Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


# ✅ game_state.py 또는 main 루프에 추가할 함수
import game_state

def calculate_total_profit():
    total_invested = 0.0
    total_value = 0.0
    for ticker, data in game_state.portfolio["stocks"].items():
        qty = data["quantity"]
        if qty > 0:
            invested = qty * data["buy_price"]
            index = game_state.time_indices.get(ticker, 0)
            current_price = game_state.prices_by_ticker.get(f"{ticker}_Close", [0])[index]
            value = qty * current_price
            total_invested += invested
            total_value += value
    return total_value - total_invested


# ✅ 세금, 배당 등 적용

def apply_tax_or_dividend():
    day = game_state.current_day_index
    if day > 0 and day % 30 == 0:
        tax = game_state.portfolio['cash'] * 0.02
        game_state.portfolio['cash'] -= tax
        game_state.alerts.append((f"Tax deducted: ${tax:.2f}", time.time()))

    if day > 0 and day % 60 == 0:
        game_state.portfolio['cash'] += 100
        game_state.alerts.append((f"Dividend received: $100", time.time()))
