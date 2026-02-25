import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image, ImageOps

# 1. Настройка страницы
st.set_page_config(page_title="ARBITRAGE OS v12.1", layout="wide")

# 2. Кастомный стиль
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stMetricValue"] { color: #39FF14 !important; }
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
st.title("🛰️ ARBITRAGE OS v12.1")

t1, t2, t3 = st.tabs(["📊 ЭКОНОМИКА", "🖼️ КРЕАТИВЫ", "💎 ОФФЕРЫ"])

# --- ВКЛАДКА 1: ЭКОНОМИКА ---
with t1:
    st.subheader("Расчет доходности")
    c_in, c_res = st.columns([2, 1])
    with c_in:
        p_curr = st.selectbox("Валюта выплаты", ["USD", "EUR", "RUB", "KZT", "UAH"], key="pc")
        p_val = st.number_input(f"Выплата ({p_curr})", value=25.0)
        st.divider()
        t_curr = st.selectbox("Валюта расхода", ["USD", "KZT", "RUB", "UAH", "EUR"], key="tc")
        cc1, cc2 = st.columns(2)
        cr = cc1.number_input("CR (%)", value=2.0)
        ap = cc2.number_input("Approve (%)", value=40.0)
    
    # Расчеты
    r_p = get_rate(p_curr)
    r_t = get_rate(t_curr)
    be_usd = (p_val / r_p) * (cr / 100) * (ap / 100)
    be_local = be_usd * r_t
    
    with c_res:
        st.metric(f"МАКС. CPC ({t_curr})", round(be_local, 3))
        st.metric("ROI 100% CPC", round(be_local/2, 3))
        st.caption(f"Курсы: {p_curr}={r_p} / {t_curr}={r_t}")

# --- ВКЛАДКА 2: КРЕАТИВЫ ---
with t2:
    st.subheader("Уникализатор")
    up = st.file_uploader("Фото", type=['jpg', 'png'])
    if up:
        img = Image.open(up)
        num = st.slider("Копии", 1, 5, 3)
        if st.button("ПУСК"):
            cols = st.columns(num)
            for i in range(num):
                out = img.rotate(random.uniform(-1.5, 1.5))
                if random.choice([True, False]): out = ImageOps.mirror(out)
                cols[i].image(out, use_container_width=True)
                buf = io.BytesIO()
                out.save(buf, format="JPEG", quality=90)
                cols[i].download_button(f"Save {i}", buf.getvalue(), f"cr_{i}.jpg", key=f"d{i}")

# --- ВКЛАДКА 3: ОФФЕРЫ ---
with t3:
    st.subheader("Leadbit API")
    tkn = st.text_input("API Token", type="password")
    geo = st.text_input("ГЕО (пусто = ВСЕ)", "").upper()
    
    if st.button("🔥 ЗАГРУЗИТЬ"):
        if tkn:
            try:
                with st.spinner("Загрузка..."):
                    res = httpx.get(f"https://leadbit.com/api/offer/list?token={tkn}", timeout=15)
                    d = res.json()
                    if d.get('status') == 'success':
                        offs = d.get('data', [])
                        if geo:
                            offs = [o for o in offs if any(c['code'] == geo for c in o.get('countries', []))]
                        if offs:
                            st.dataframe(pd.DataFrame(offs)[['name', 'payout', 'currency', 'status']], use_container_width=True)
                        else:
                            st.warning("Ничего не найдено")
                    else:
                        st.error(f"Leadbit Error: {d.get('message')}")
            except Exception as e:
                st.error(f"Network Error: {e}")
        else:
            st.warning("Вставь токен")
