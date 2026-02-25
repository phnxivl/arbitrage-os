import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image, ImageOps

# 1. Инициализация (используем st.set_page_config из твоего списка)
st.set_page_config(page_title="ARBITRAGE OS PRO", layout="wide")

# 2. Кастомный стиль через Markdown
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stMetricValue"] { color: #39FF14 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Функция для валют (используем httpx для скорости)
def get_rate(currency_code):
    if currency_code == "USD": return 1.0
    try:
        r = httpx.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        return r.json()['rates'].get(currency_code, 1.0)
    except:
        return 1.0

# 4. Заголовок
st.title("🛰️ ARBITRAGE OS v10.0")

# 5. Создаем табы (метод st.tabs из твоего списка)
t_calc, t_creo, t_offers = st.tabs(["📊 ЭКОНОМИКА", "🖼️ КРЕАТИВЫ", "💎 ОФФЕРЫ"])

# --- ВКЛАДКА 1: КАЛЬКУЛЯТОР ---
with t_calc:
    st.subheader("Расчет доходности")
    
    # Сетка через st.columns
    c1, c2 = st.columns([2, 1])
    
    with c1:
        # Выбор валюты (метод st.selectbox)
        curr = st.selectbox("Валюта", ["USD", "RUB", "KZT", "UAH", "EUR"])
        
        # Ввод чисел (метод st.number_input)
        pay = st.number_input("Выплата за лид ($)", value=25.0)
        cr = st.number_input("CR лендинга (%)", value=2.0)
        app = st.number_input("Аппрув (%)", value=40.0)
        
    # Математика
    rate = get_rate(curr)
    be_usd = pay * (cr / 100) * (app / 100)
    be_local = be_usd * rate
    
    with c2:
        # Вывод метрик (метод st.metric)
        st.metric(f"МАКС. CPC ({curr})", f"{round(be_local, 3)}")
        st.metric("ROI 100% CPC", f"{round(be_local/2, 3)}")
        st.info(f"Курс: 1$ = {rate} {curr}")

# --- ВКЛАДКА 2: КРЕАТИВЫ ---
with t_creo:
    st.subheader("Уникализатор метаданных и визуала")
    # Загрузка файла (метод st.file_uploader)
    file = st.file_uploader("Загрузи крео", type=['jpg', 'png'])
    
    if file:
        img = Image.open(file)
        # Слайдер (метод st.slider)
        num = st.slider("Сколько копий?", 1, 5, 3)
        
        if st.button("ПУСК"):
            cols = st.columns(num)
            for i in range(num):
                # Рандомная уникализация
                out = img.rotate(random.uniform(-1.5, 1.5))
                if random.choice([True, False]):
                    out = ImageOps.mirror(out)
                
                cols[i].image(out, use_container_width=True)
                
                # Скачивание (метод st.download_button)
                buf = io.BytesIO()
                out.save(buf, format="JPEG", quality=90)
                cols[i].download_button(f"Save #{i+1}", buf.getvalue(), f"ready_{i+1}.jpg", key=f"d{i}")

# --- ВКЛАДКА 3: ОФФЕРЫ ---
with t_offers:
    st.subheader("Leadbit API Connect")
    token = st.text_input("API Token", type="password")
    geo = st.text_input("ГЕО код (напр. KZ)", "KZ")
    
    if st.button("ПОЛУЧИТЬ ДАННЫЕ"):
        if token:
            try:
                # Индикатор загрузки (метод st.spinner)
                with st.spinner("Связь с сервером..."):
                    res = httpx.get(f"https://leadbit.com/api/offer/list?token={token}")
                    data = res.json().get('data', [])
                    # Фильтруем
                    f = [o for o in data if any(c['code'] == geo.upper() for c in o.get('countries', []))]
                    if f:
                        # Таблица (метод st.dataframe)
                        st.dataframe(pd.DataFrame(f)[['name', 'payout', 'status']], use_container_width=True)
                    else:
                        st.warning("Нет офферов под это ГЕО")
            except:
                st.error("Ошибка API")
