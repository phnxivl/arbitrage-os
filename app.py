import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image, ImageOps

# 1. Жесткая настройка (всегда первая)
st.set_page_config(page_title="ARBITRAGE OS v8.0", layout="centered")

# 2. Дизайн
st.markdown("<style>.stMetric { background-color: #1a1a1a; padding: 10px; border-radius: 10px; }</style>", unsafe_allow_html=True)

st.title("🛰️ ARBITRAGE OS v8.0")

# 3. ТАБЫ
tab_calc, tab_creo, tab_api = st.tabs(["📊 КАЛЬКУЛЯТОР", "🖼️ КРЕАТИВЫ", "💎 ОФФЕРЫ"])

# --- ВКЛАДКА КАЛЬКУЛЯТОРА ---
with tab_calc:
    st.header("Расчет прибыли")
    payout = st.number_input("Выплата ($)", min_value=0.0, value=25.0, step=1.0, key="p1")
    cr = st.number_input("CR лендинга (%)", min_value=0.0, value=2.0, step=0.1, key="c1")
    approve = st.number_input("Аппрув (%)", min_value=0.0, value=40.0, step=1.0, key="a1")
    
    cpc_usd = payout * (cr / 100) * (approve / 100)
    
    st.divider()
    st.metric(label="МАКСИМАЛЬНЫЙ CPC ($)", value=f"${round(cpc_usd, 3)}")
    st.metric(label="ДЛЯ ROI 100% ($)", value=f"${round(cpc_usd/2, 3)}")
    st.info("Калькулятор активен")

# --- ВКЛАДКА КРЕАТИВОВ ---
with tab_creo:
    st.header("Уникализатор")
    file = st.file_uploader("Загрузи картинку", type=['jpg', 'png'])
    if file:
        img = Image.open(file)
        if st.button("СДЕЛАТЬ КОПИЮ"):
            out = img.rotate(random.randint(-2, 2))
            out = ImageOps.mirror(out)
            st.image(out, caption="Готовый крео", width=300)
            buf = io.BytesIO()
            out.save(buf, format="JPEG")
            st.download_button("СКАЧАТЬ", buf.getvalue(), "unique.jpg")

# --- ВКЛАДКА API ---
with tab_api
