import datetime

news_events = [
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

active_events = []
