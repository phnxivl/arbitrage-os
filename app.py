import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image, ImageOps

# 1. Настройка страницы (СТРОГО ПЕРВАЯ СТРОКА)
st.set_page_config(page_title="ARBITRAGE OS v9.0", layout="wide")

# 2. Дизайн: Dark Mode и яркие метрики
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stMetricValue"] { color: #39FF14 !important; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #21262D; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Функция получения курса валют
def get_rate(target_currency):
    if target_currency == "USD": return 1.0
    try:
        # Прямой запрос курса без кэширования для надежности
        r = httpx.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        return r.json()['rates'].get(target_currency, 1.0)
    except:
        return 1.0

# --- ГЛАВНЫЙ ИНТЕРФЕЙС ---
st.title("🛰️ ARBITRAGE OS: ПОЛНАЯ ВЕРСИЯ")

tabs = st.tabs(["📊 КАЛЬКУЛЯТОР", "🖼️ КРЕАТИВЫ", "💎 ОФФЕРЫ"])

# --- ВКЛАДКА 1: КАЛЬКУЛЯТОР (С ВАЛЮТАМИ) ---
with tabs[0]:
    st.header("Юнит-экономика и Валюты")
    
    col_input, col_res = st.columns([2, 1])
    
    with col_input:
        curr_list = ["USD", "RUB", "KZT", "UAH", "EUR"]
        target_curr = st.selectbox("Валюта расчета", curr_list, key="c_sel")
        
        c1, c2, c3 = st.columns(3)
        p_usd = c1.number_input("Выплата ($)", min_value=0.0, value=25.0, step=1.0)
        cr = c2.number_input("CR ленда (%)", min_value=0.0, value=2.0, step=0.1)
        ap = c3.number_input("Аппрув (%)", min_value=0.0, value=40.0, step=1.0)
        
    # Расчет курса
    rate = get_rate(target_curr)
    be_usd = p_usd * (cr / 100) * (ap / 100)
    be_local = be_usd * rate
    
    with col_res:
        st
