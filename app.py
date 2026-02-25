import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image
from engine import hardcore_unique, calculate_be_cpc

# 1. Настройки
st.set_page_config(page_title="ARBITRAGE OS", layout="wide")

# 2. Стиль
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stMetricValue"] { color: #39FF14 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Функции
def get_rate(curr):
    if curr == "USD": return 1.0
    try:
        r = httpx.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        return r.json()['rates'].get(curr, 1.0)
    except: return 1.0

# 4. Интерфейс
st.title("⚡ ARBITRAGE OS v4.5")
tabs = st.tabs(["🚀 ОФФЕРЫ", "🎨 КРЕАТИВЫ", "📊 КАЛЬКУЛЯТОР"])

with tabs[0]:
    tkn = st.text_input("LEADBIT TOKEN", type="password")
    geo = st.text_input("ГЕО", "KZ")
    if st.button("ОБНОВИТЬ"):
        if tkn:
            try:
                res = httpx.get(f"https://leadbit.com/api/offer/list?token={tkn}")
                df = pd.DataFrame(res.json().get('data', []))
                st.table(df[['name', 'payout', 'status']].head(10))
            except: st.error("Ошибка API")

with tabs[1]:
    up = st.file_uploader("Загрузи фото", type=['jpg', 'png'])
    if up:
        img = Image.open(up)
        if st.button("УНИКАЛИЗИРОВАТЬ"):
            res_img = hardcore_unique(img)
            st.image(res_img, width=400)
            buf = io.BytesIO()
            res_img.save(buf, format="JPEG")
            st.download_button("СКАЧАТЬ", buf.getvalue(), "ready.jpg")

with tabs[2]:
    curr = st.selectbox("Валюта", ["USD", "RUB", "KZT", "UAH"])
    rate = get_rate(curr)
    c1, c2, c3 = st.columns(3)
