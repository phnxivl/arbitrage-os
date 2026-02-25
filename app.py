import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image
from engine import hardcore_unique, calculate_be_cpc

# --- КОНФИГУРАЦИЯ И СТИЛЬ ---
st.set_page_config(page_title="ARBITRAGE OS v4.5", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: #161B22; padding: 10px 20px; border-radius: 15px 15px 0 0; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; border-radius: 4px; color: #8B949E; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: #58A6FF !important; border-bottom: 2px solid #58A6FF !important; }
    div[data-testid="stMetricValue"] { font-size: 2.2rem; color: #39FF14; text-shadow: 0 0 10px rgba(57, 255, 20, 0.3); }
    .stButton>button { width: 100%; border-radius: 10px; border: 1px solid #30363D; background-color: #21262D; color: #C9D1D9; transition: 0.3s; }
    .stButton>button:hover { border-color: #58A6FF; color: #58A6FF; box-shadow: 0 0 15px rgba(88, 166, 255, 0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- ФУНКЦИЯ КУРСА ВАЛЮТ ---
def get_exchange_rate(target_currency):
    if target_currency == "USD": return 1.0
    try:
        # Используем бесплатное API для курсов
        r = httpx.get("https://open.er-api.com/v6/latest/USD")
        return r.json()['rates'].get(target_currency, 1.0)
    except:
        return 1.0

# --- ШАПКА ---
col_logo, col_stat = st.columns([1, 4])
with col_logo:
    st.markdown("# ⚡ OS")
with col_stat:
    st.markdown("### `СТАТУС СИСТЕМЫ: АКТИВНА` | `РЕЖИМ: АГРЕССИВНЫЙ Б
