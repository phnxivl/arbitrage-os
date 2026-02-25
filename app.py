import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image, ImageOps, ImageFilter

# 1. Настройки и стиль
st.set_page_config(page_title="ARBITRAGE OS PRO", layout="wide", page_icon="📈")
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
    .stTabs [data-baseweb="tab-list"] { background-color: #161B22; border-radius: 10px; padding: 5px; }
    .stMetric { background-color: #1A1F29; padding: 15px; border-radius: 10px; border: 1px solid #30363D; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; text-shadow: 0 0 10px rgba(0,255,65,0.4); }
    .stButton>button { background: linear-gradient(45deg, #0052D4, #4364F7, #6FB1FC); border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Движок уникализации
def process_batch(image, count=5):
    results = []
    for _ in range(count):
        temp = image.rotate(random.uniform(-2, 2))
        if random.choice([True, False]):
            temp = ImageOps.mirror(temp)
        temp = temp.filter(ImageFilter.SHARPEN)
        results.append(temp)
    return results

# 3. Интерфейс
st.title("🛰️ ARBITRAGE OS: PRO TERMINAL")
tabs = st.tabs(["💎 OFFERS", "🖼️ BATCH CREATIVE", "📝 SPY TEXTS", "📊 ECONOMY"])

# --- ВКЛАДКА 1: LEADBIT ---
with tabs[0]:
    st.subheader("Мониторинг Офферов")
    c1, c2 = st.columns([3, 1])
    tkn = c1.text_input("Leadbit API Token", type="password")
    geo_filter = c2.text_input("ГЕО", "KZ")
    if st.button("ОБНОВИТЬ СПИСОК"):
        try:
            r = httpx.get(f"https://leadbit.com/api/offer/list?token={tkn}", timeout=10)
            data = r.json().get('data', [])
            filtered = [o for o in data if any(c['code'] == geo_filter.upper() for c in o.get('countries', []))]
            st.dataframe(pd.DataFrame(filtered)[['name', '
