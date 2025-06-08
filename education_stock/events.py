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
        "end_date": datetime.date(2025, 12, 31)
    }
]

# ✅ 랜덤 뉴스 이벤트 리스트
random_events = []

def schedule_random_events(tickers, simulation_dates):
    """
    각 종목마다 달에 1개 이상 랜덤 뉴스 이벤트 생성
    """
    global random_events
    random_events = []

    if not simulation_dates:
        raise ValueError("❌ simulation_date_list가 비어 있음")

    # ✅ 날짜들을 (year, month) 기준으로 그룹화
    date_by_month = {}
    for d in simulation_dates:
        ym = (d.year, d.month)
        if ym not in date_by_month:
            date_by_month[ym] = []
        date_by_month[ym].append(d)

    # ✅ 뉴스 템플릿 정의
    news_templates = [
        ("good", +0.05, "{} reports record earnings 📈"),
        ("bad", -0.05, "{} under investigation ⚖️"),
        ("neutral", 0.0, "{} holds steady with market."),
        ("bad", -0.08, "{} faces production delays 🏭"),
        ("good", +0.08, "{} signs major partnership deal 🤝"),
        ("bad", -0.07, "{} suffers from CEO controversy 👤"),
        ("good", +0.1, "{} launches new flagship product 🚀"),
    ]

    # ✅ 각 티커 × 월 별로 뉴스 생성
    for ticker in tickers:
        for ym, dates in date_by_month.items():
            chosen_date = random.choice(dates)
            effect_type, impact, template = random.choice(news_templates)
            message = template.format(ticker)
            random_events.append({
                "date": chosen_date,
                "ticker": ticker,
                "effect": impact,
                "message": message
            })

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
    """지속 노출되어야 하는 뉴스 이벤트 목록 반환"""
    results = []
    for event in persistent_events:
        if event["start_date"] <= current_date <= event["end_date"]:
            results.append(f"📌 {event['ticker']} - {event['title']}")
    return results
