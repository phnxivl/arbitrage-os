import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image, ImageOps, ImageFilter

# 1. Настройки (СТРОГО ПЕРВЫМИ)
st.set_page_config(page_title="ARBITRAGE OS PRO", layout="wide")

# 2. Облегченный дизайн
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161B22; }
    </style>
    """, unsafe_allow_html=True)

# 3. Функции (вынесены, чтобы не тормозить запуск)
def get_rate_safe(c):
    if c == "USD": return 1.0
    try:
        r = httpx.get("https://open.er-api.com/v6/latest/USD", timeout=1.5)
        return r.json()['rates'].get(c, 1.0)
    except: return 1.0

def process_batch_safe(img, count):
    res = []
    for _ in range(count):
        temp = img.rotate(random.uniform(-1.5, 1.5))
        if random.choice([True, False]): temp = ImageOps.mirror(temp)
        res.append(temp.filter(ImageFilter.SMOOTH))
    return res

# 4. Интерфейс
st.title("🛰️ ARBITRAGE OS v6.1")

t = st.tabs(["📊 ЭКОНОМИКА", "🖼️ КРЕАТИВЫ", "💎 ОФФЕРЫ", "📝 ТЕКСТЫ"])

# --- ВКЛАДКА 1: ЭКОНОМИКА (Самая важная) ---
with t[0]:
    st.subheader("Калькулятор ROI")
    c1, c2, c3 = st.columns(3)
    p = c1.number_input("Выплата ($)", value=25.0, key="p")
