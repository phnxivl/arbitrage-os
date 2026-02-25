import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image, ImageOps, ImageFilter

# 1. Настройки страницы
st.set_page_config(page_title="ARBITRAGE OS v5.0", layout="wide")

# 2. Дизайн
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stMetricValue"] { color: #39FF14 !important; font-size: 3rem !important; }
    .stNumberInput input { background-color: #161B22 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Вспомогательные функции (теперь они прямо здесь)
def get_rate(curr):
    if curr == "USD": return 1.0
    try:
        r = httpx.get("https://open.er-api.com/v6/latest/USD", timeout=2)
        return r.json()['rates'].get(curr, 1.0)
    except: return 1.0

def fast_unique(image):
    img = image.rotate(random.uniform(-1.5, 1.5))
    if random.choice([True, False]):
        img = ImageOps.mirror(img)
    return img.filter(ImageFilter.SMOOTH_MORE)

# 4. Интерфейс
st.title("⚡ ARBITRAGE COMMAND CENTER")

tabs = st.tabs(["🚀 ОФФЕРЫ", "🎨 КРЕАТИВЫ", "📊 КАЛЬКУЛЯТОР"])

with tabs[0]:
    st.subheader("Leadbit API")
    tkn = st.text_input("Токен", type="password", key="tkn_field")
    if st.button("Загрузить данные"):
        st.info("Подключаюсь к Leadbit...")
        # Тут логика API

with tabs[1]:
    st.subheader("Уникализатор")
    up = st.file_uploader("Загрузи фото", type=['jpg', 'png'])
    if up:
        img = Image.open(up)
        if st.button("Сделать уникальным"):
            res = fast_unique(img)
            st.image(res, width=400)

with tabs[2]:
    st.subheader("💰 Калькулятор Профита")
    
    curr = st.selectbox("Валюта", ["USD", "RUB", "KZT", "UAH"], key="curr_sel")
    rate = get_rate(curr)
    
    col1, col2, col3 = st.columns(3)
    # Используем простые переменные для мгновенного расчета
    payout = col1.number_input("Выплата ($)", value=20.0, step=1.0, key="p_val")
    cr = col2.number_input("CR лендинга (%)", value=2.0, step=0.1, key="cr_val")
    approve = col3.number_input("Аппрув (%)", value=30.0, step=1.0, key="ap_val")
    
    # Считаем прямо тут
    result_usd = payout * (cr / 100) * (approve / 100)
    result_local = result_usd * rate
    
    st.divider()
    
    c1, c2 = st.columns(2)
    c1.metric(f"МАКС. CPC ({curr})", f"{round(result_local, 3)}")
    c2.metric(f"ДЛЯ ROI 100% ({curr})", f"{round(result_local/2, 3)}")
    
    st.write(f"Курс: 1$ = {rate} {curr}")
