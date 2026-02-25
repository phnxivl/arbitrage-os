import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image, ImageOps

# 1. Инициализация переменных сессии (чтобы не было ошибок NameError)
if 'p_val_auto' not in st.session_state:
    st.session_state['p_val_auto'] = 25.0
if 'p_curr_auto' not in st.session_state:
    st.session_state['p_curr_auto'] = "USD"

# 2. Настройка страницы
st.set_page_config(page_title="ARBITRAGE OS v13.0", layout="wide")

# 3. Стиль
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stMetricValue"] { color: #39FF14 !important; }
    .stDataFrame { background-color: #161B22; }
    </style>
    """, unsafe_allow_html=True)

# 4. Функция валют
def get_rate(currency_code):
    if currency_code == "USD": return 1.0
    try:
        r = httpx.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        return r.json()['rates'].get(currency_code, 1.0)
    except:
        return 1.0

st.title("🛰️ ARBITRAGE OS v13.0 PRO")

t_calc, t_creo, t_offers = st.tabs(["📊 ЭКОНОМИКА", "🖼️ КРЕАТИВЫ", "💎 ОФФЕРЫ"])

# --- ВКЛАДКА 1: ЭКОНОМИКА ---
with t_calc:
    st.subheader("Расчет доходности")
    c_in, c_res = st.columns([2, 1])
    
    with c_in:
        # Берем значения из сессии, если они там есть
        currencies = ["USD", "EUR", "RUB", "KZT", "UAH"]
        default_curr_idx = currencies.index(st.session_state['p_curr_auto']) if st.session_state['p_curr_auto'] in currencies else 0
        
        p_curr = st.selectbox("Валюта выплаты", currencies, index=default_curr_idx, key="pc")
        p_val = st.number_input(f"Выплата ({p_curr})", value=float(st.session_state['p_val_auto']), key="pv")
        
        st.divider()
        t_curr = st.selectbox("Валюта расхода (закупка)", ["USD", "KZT", "RUB", "UAH", "EUR"], key="tc")
        
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
        st.info(f"Конвертация: {p_val} {p_curr} -> {round(p_val/r_p, 2)} USD")

# --- ВКЛАДКА 2: КРЕАТИВЫ ---
with t_creo:
    st.subheader("Уникализатор")
    up = st.file_uploader("Загрузи фото", type=['jpg', 'png'])
    if up:
        img = Image.open(up)
        num = st.slider("Количество копий", 1, 5, 3)
        if st.button("ПУСК"):
            cols = st.columns(num)
            for i in range(num):
                out = img.rotate(random.uniform(-1.5, 1.5))
                if random.choice([True, False]): out = ImageOps.mirror(out)
                cols[i].image(out, use_container_width=True)
                buf = io.BytesIO()
                out.save(buf, format="JPEG", quality=90)
                cols[i].download_button(f"Save {i}", buf.getvalue(), f"ready_{i}.jpg", key=f"d{i}")

# --- ВКЛАДКА 3: ОФФЕРЫ (С ПОДКЛЮЧЕНИЕМ К КАЛЬКУЛЯТОРУ) ---
with t_offers:
    st.subheader("Leadbit API Explorer")
    tkn = st.text_input("API Token", type="password", key="tkn_field")
    geo = st.text_input("ГЕО фильтр", "").upper()
    
    if st.button("🔥 ПОЛУЧИТЬ ОФФЕРЫ"):
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
                            # Сохраняем в session_state для выбора
                            st.session_state['current_offers'] = offs
                            st.success(f"Найдено {len(offs)} офферов")
                        else:
                            st.warning("Офферы не найдены")
                    else:
                        st.error(f"Ошибка Leadbit: {d.get('message')}")
            except Exception as e:
                st.error(f"Ошибка сети: {e}")
    
    # Если офферы загружены, показываем выбор
    if 'current_offers' in st.session_state:
        df = pd.DataFrame(st.session_state['current_offers'])
        
        selected_offer_name = st.selectbox("Выберите оффер для экспорта:", df['name'].tolist())
        
        if st.button("📥 ПЕРЕНЕСТИ В КАЛЬКУЛЯТОР"):
            selected_row = df[df['name'] == selected_offer_name].iloc[0]
            st.session_state['p_val_auto'] = float(selected_row['payout'])
            st.session_state['p_curr_auto'] = selected_row['currency']
            st.success(f"Оффер '{selected_offer_name}' подключен! Переходи во вкладку ЭКОНОМИКА.")
            st.rerun() # Перезапуск для обновления инпутов

        st.divider()
        st.dataframe(df[['name', 'payout', 'currency', 'status']], use_container_width=True)
