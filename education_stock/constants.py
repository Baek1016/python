# constants.py

import datetime

# ✅ TICKERS (전세계 주식)
TICKERS = {
    # 미국
    'AAPL': 'Apple', 'GOOG': 'Google', 'TSLA': 'Tesla', 'MSFT': 'Microsoft', 'AMZN': 'Amazon',
    'META': 'Meta', 'NFLX': 'Netflix', 'NVDA': 'Nvidia', 'INTC': 'Intel', 'AMD': 'AMD',
    'DIS': 'Disney', 'IBM': 'IBM', 'ORCL': 'Oracle', 'PYPL': 'PayPal', 'ADBE': 'Adobe',
    'QCOM': 'Qualcomm', 'KO': 'CocaCola', 'PEP': 'PepsiCo', 'WMT': 'Walmart',
    'JNJ': 'Johnson & Johnson', 'V': 'Visa', 'MA': 'Mastercard',

    # 한국
    '005930.KS': 'Samsung Electronics', '066570.KS': 'LG Electronics',
    '005380.KS': 'Hyundai Motor', '035420.KS': 'Naver', '035720.KS': 'Kakao',

    # 홍콩
    '9988.HK': 'Alibaba', '0700.HK': 'Tencent', '1810.HK': 'Xiaomi',

    # 일본
    '6758.T': 'Sony', '9984.T': 'SoftBank', '7203.T': 'Toyota',

    # 유럽
    'AIR.PA': 'Airbus', 'OR.PA': 'L’Oreal', 'SIE.DE': 'Siemens',
    'BMW.DE': 'BMW', 'SAP.DE': 'SAP',

    # 브라질
    'VALE': 'Vale (Brazil)', 'PBR': 'Petrobras (Brazil)',

    # 캐나다
    'SHOP': 'Shopify', 'RY': 'Royal Bank of Canada',

    # 인도
    'RELIANCE.NS': 'Reliance'
}

# ✅ 회사별 색상
COMPANY_COLORS = {
    'AAPL': (255, 99, 132), 'GOOG': (54, 162, 235), 'TSLA': (255, 206, 86),
    'MSFT': (75, 192, 192), 'AMZN': (153, 102, 255), 'META': (255, 159, 64),
    'NFLX': (199, 199, 199), 'NVDA': (83, 102, 255), 'INTC': (255, 99, 255),
    'AMD': (99, 255, 132), 'DIS': (100, 100, 100), 'IBM': (255, 70, 70),
    'ORCL': (0, 230, 115), 'PYPL': (204, 204, 0), 'ADBE': (0, 153, 153),
    'QCOM': (102, 0, 204), 'KO': (255, 51, 0)
}

# ✅ 차트 레이아웃 등 UI 레이아웃 설정
LAYOUT = {
    "screen": {"width": 1600, "height": 900},
    "chart": {"x": 478, "y": 50, "width": 751, "height": 268},
    "buttons": {
        "buy": {"width": 136, "height": 45, "offset_x": -341},
        "sell": {"width": 136, "height": 45, "offset_x": -163},
        "offset_y": 15
    },
    "stock_list": {
        "x": 30, "y_start": 100, "button_height": 35, "visible_height": 300,
        "title_x": 30, "title_y": 60
    },
    "grid": {
        "x": 30, "y_offset_from_bottom": 10,
        "cols": 5, "rows": 10,
        "cell_width": 273, "cell_height": 35
    },
    "portfolio": {
        "x": -273, "y_start": 100, "visible_height": 400, "line_height": 25
    },
    "alerts": {"x": 614, "y_base": 668, "line_height": 20, "max": 3},
    "profit_summary": {"x": -273, "y": 10},
    "rank_chart": {
        "x_from_grid": True,
        "offset_from_grid_x": 40,
        "offset_y": -15,
        "width": 683,
        "extra_height": 20
    },
    "cash": {"x": 30, "y": 30},
    "news": {
        "x": 1200, "y": 300,
        "width": 360,
        "max_lines": 10
    },
    "longterm_news": {
    "x": 950,  # 원하는 위치로 조절 가능
    "y": 60
}

}
