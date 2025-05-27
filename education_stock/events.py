# events.py
import random
import datetime

# ✅ 고정 뉴스 이벤트 리스트
fixed_events = [
    {
        "date": datetime.date(2023, 5, 30),
        "ticker": "TSLA",
        "title": "Tesla CEO 사임 발표",
        "effect_days": [1],
        "impact": -0.1
    },
    {
        "date": datetime.date(2023, 6, 3),
        "ticker": "MSFT",
        "title": "MS Office 무료화 루머",
        "effect_days": [0, 1, 2],
        "impact": +0.05
    }
]

# ✅ 장기 유지되는 루머성 뉴스
persistent_events = [
    {
        "ticker": "MSFT",
        "title": "MS Office 무료화 루머",
        "impact": +0.05,
        "start_date": datetime.date(2023, 6, 3),
        "end_date": datetime.date(2025, 12, 31)  # 계속 유지되는 효과
    }
]

# ✅ 랜덤 뉴스 이벤트 리스트
random_events = []

def schedule_random_events(tickers, simulation_dates, count=100):
    """
    특정 종목들에 대해 랜덤 뉴스 이벤트를 simulation_dates 내에서 생성한다.
    """
    global random_events
    if not simulation_dates:
        raise ValueError("⚠ simulation_date_list가 비어 있어서 뉴스 이벤트 날짜를 선택할 수 없습니다.")

    def generate_random_news(ticker):
        effects = [
            ("good", 0.05, f"{ticker} releases strong earnings! 📈"),
            ("bad", -0.05, f"{ticker} hit by regulatory issues. 📉"),
            ("neutral", 0.0, f"{ticker} holds steady with market.")
        ]
        effect_type, change, message = random.choice(effects)
        valid_dates = simulation_dates[10:] if len(simulation_dates) > 10 else simulation_dates
        date = random.choice(valid_dates)
        return {
            "date": date,
            "ticker": ticker,
            "effect": change,
            "message": message
        }

    random_events = [generate_random_news(ticker) for ticker in random.sample(tickers, min(len(tickers), count))]

def get_events_for_date(date):
    """해당 날짜에 발생하는 모든 고정 + 랜덤 뉴스 반환"""
    results = []

    # ✅ 고정 뉴스 처리
    for event in fixed_events:
        for offset in event["effect_days"]:
            if event["date"] + datetime.timedelta(days=offset) == date:
                results.append({
                    "ticker": event["ticker"],
                    "impact": event["impact"],
                    "message": f"[FIXED] {event['title']} (영향: {event['impact']*100:+.1f}%)"
                })

    # ✅ 랜덤 뉴스 처리
    for event in random_events:
        if event["date"] == date:
            results.append({
                "ticker": event["ticker"],
                "impact": event["effect"],
                "message": f"[RANDOM] {event['message']} (영향: {event['effect']*100:+.1f}%)"
            })

    return results

def get_persistent_events(current_date):
    """지속 노출되어야 하는 뉴스 이벤트 목록 반환 (루머 등)"""
    results = []
    for event in persistent_events:
        if event["start_date"] <= current_date <= event["end_date"]:
            results.append(f"📌 {event['ticker']} - {event['title']}")
    return results
