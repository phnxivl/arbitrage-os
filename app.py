import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image
from engine import hardcore_unique, calculate_be_cpc

# 1. Настройки страницы (строго в начале)
st.set_page_config(page_title="ARBITRAGE OS", layout="wide")

# 2. Упрощенный дизайн (без лишних скриптов)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stMetricValue"] { color: #39FF14 !important; }
    .stButton>button { border-radius: 20px; height: 3em; background-color: #21262D; }
    </style>
    """, unsafe_allow_html=True)

# 3. Функции
def get_rate(curr):
    if curr == "USD": return 1.0
    try:
        with httpx.Client() as client:
            r = client.get("https://open.er-api.com/v6/latest/USD", timeout=2)
            return r.json()['rates'].get(curr, 1.0)
    except:
        return 1.0

# 4. Интерфейс
st.title("⚡ ARBITRAGE OS v4.5")

tabs = st.tabs(["🚀 ОФФЕРЫ", "🎨 КРЕАТИВЫ", "📊 КАЛЬКУЛЯТОР"])

with tabs[0]:
    c1, c2 = st.columns(2)
    token = c1.text_input("LEADBIT TOKEN", type="password")
    geo = c2.text_input("ГЕО", "KZ")
    
    if st.button("ОБНОВИТЬ СПИСОК"):
        if token:
            try:
                res = httpx.get(f"https://leadbit.com/api/offer/list?token={token}", timeout=10)
                data = res.json().get('data', [])
                if data:
                    df = pd.DataFrame(data)
                    st.table(df[['name', 'payout', 'status']].head(10))
                else:
                    st.warning("Пусто.")
            except:
                st.error("Ошибка API")

with tabs[1]:
    st.subheader("Уникализатор")
    file = st.file_uploader("Загрузи фото", type=['jpg', 'png'])
    if file:
        img = Image.open(file)
        if st.button("УНИКАЛИЗИРОВАТЬ"):
            processed = hardcore_unique(img)
            st.image(processed, width=400)
            buf = io.BytesIO()
            processed.save(buf, format="JPEG")
            st.download_button("СКАЧАТЬ", buf.getvalue(), "ready.jpg")

with tabs[2]:
    st.subheader("Расчет профита")
    curr = st.selectbox("Валюта", ["USD", "RUB", "KZT", "UAH"])
    rate = get_rate(curr)
    
    col1, col2, col3 = st.columns(3)
    p = col1.number_input("Выплата ($)", value=20.0)
    cr = col2.number_input("CR (%)", value=2.0)
    ap = col3.number_input("Аппрув (%)", value=
