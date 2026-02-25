import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image, ImageOps

# 1. Настройка страницы
st.set_page_config(page_title="ARBITRAGE OS v12.0", layout="wide")

# 2. Кастомный стиль
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stMetricValue"] { color: #39FF14 !important; }
    .stDataFrame { background-color: #161B22; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Функция для валют
def get_rate(currency_code):
    if currency_code == "USD": return 1.0
    try:
        r = httpx.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        return r.json()['rates'].get(currency_code, 1.0)
    except:
        return 1.0

# 4. Заголовок
st.title("🛰️ ARBITRAGE OS v12.0")

# 5. Создаем табы
t_calc, t_creo, t_offers = st.tabs(["📊 ЭКОНОМИКА", "🖼️ КРЕАТИВЫ", "💎 ОФФЕРЫ"])

# --- ВКЛАДКА 1: ЭКОНОМИКА ---
with t_calc:
    st.subheader("Расчет доходности")
    col_input, col_res = st.columns([2, 1])
    with col_input:
        payout_curr = st.selectbox("Валюта выплаты", ["USD", "EUR", "RUB", "KZT", "UAH"], key="p_curr")
        pay_val = st.number_input(f"Сумма выплаты ({payout_curr})", value=25.0, step=1.0)
        st.divider()
        target_curr = st.selectbox("Валюта расхода (закупка)", ["USD", "KZT", "RUB", "UAH", "EUR"], key="t_curr")
        cc1, cc2 = st.columns(2)
        cr = cc1.number_input("CR лендинга (%)", value=2.0, step=0.1)
        app = cc2.number_input("Аппрув (%)", value=40.0, step=1.0)
    
    rate_payout = get_rate(payout_curr)
    rate_target = get_rate(target_curr)
    pay_in_usd = pay_val / rate_payout
    be_usd = pay_in_usd * (cr / 100) * (app / 100)
    be_local = be_usd * rate_target
    
    with col_res:
        st.metric(f"МАКС. CPC ({target_curr})", f"{round(be_local, 3)}")
        st.metric("ROI 100% CPC", f"{round(be_local/2, 3)}")
        st.caption(f"Курс: 1$ = {rate_payout} {payout_curr} / {rate_target} {target_curr
