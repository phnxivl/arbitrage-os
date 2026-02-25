import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image
import engine  # Импортируем наш движок

# Конфигурация страницы
st.set_page_config(page_title="ARBITRAGE OS v4.5", layout="wide", page_icon="⚡")

# Кастомный дизайн (Dark Mode)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    [data-testid="stMetricValue"] { color: #39FF14 !important; text-shadow: 0 0 10px rgba(57,255,20,0.3); }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: #161B22; padding: 10px; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #21262D; color: white; border: 1px solid #30363D; }
    .stButton>button:hover { border-color: #58A6FF; }
    </style>
    """, unsafe_allow_html=True)

# Функция курса валют
def get_rate(curr):
    if curr == "USD": return 1.0
    try:
        r = httpx.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        return r.json()['rates'].get(curr, 1.0)
    except: return 1.0

# Шапка
st.markdown("# ⚡ ARBITRAGE COMMAND CENTER")
st.markdown("`STATUS: ACTIVE` | `GEO: GLOBAL` | `CURRENCY: MULTI` ")
