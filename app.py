import streamlit as st
import pandas as pd
import httpx
import io
import random
from PIL import Image
from engine import hardcore_unique, calculate_be_cpc

# --- КОНФИГУРАЦИЯ И СТИЛЬ ---
st.set_page_config(page_title="ARBITRAGE OS v4.0", layout="wide", page_icon="⚡")

# Кастомный CSS для "охуенного" дизайна
st.markdown("""
    <style>
    /* Основной фон и шрифт */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* Стилизация вкладок (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #161B22;
        padding: 10px 20px;
        border-radius: 15px 15px 0 0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #8B949E;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #58A6FF !important;
        border-bottom: 2px solid #58A6FF !important;
    }

    /* Красивые карточки для метрик */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        color: #39FF14; /* Кислотно-зеленый */
        text-shadow: 0 0 10px rgba(57, 255, 20, 0.3);
    }

    /* Стилизация кнопок */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #30363D;
        background-color: #21262D;
        color: #C9D1D9;
        transition: 0.3s;
    }
    .stButton>button:hover {
        border-color: #58A6FF;
        color: #58A6FF;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.2);
    }

    /* Поля ввода */
    .stTextInput>div>div>input {
        background-color: #0D1117;
        border: 1px solid #30363D;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ВЕРХНЯЯ ПАНЕЛЬ ---
col_logo, col_stat = st.columns([1, 4])
with col_logo:
    st.markdown("# ⚡ OS")
with col_stat:
    st.markdown("### `SYSTEM STATUS: OPERATIONAL` | `MODE: AGGRESSIVE` ")

st.divider()

tab1, tab2, tab3 = st.tabs(["🚀 OFFERS CONTROL", "🎨 CREATIVE STUDIO", "📈 ECONOMY"])

# --- ВКЛАДКА 1: ОФФЕРЫ ---
with tab1:
    col_api, col_geo = st.columns(2)
    with col_api:
        api_token = st.text_input("LEADBIT API KEY", type="password", placeholder="Paste token here...")
    with col_geo:
        selected_geo = st.text_input("TARGET GEO", "KZ")
    
    if st.button("SYNC WITH NETWORK"):
        if api_token:
            with st.spinner("Hacking Leadbit..."):
                url = f"https://leadbit.com/api/offer/list?token={api_token}"
                try:
                    r = httpx.get(url, timeout=10)
                    offers = r.json().get('data', [])
                    filtered = [o for o in offers if any(c['code'] == selected_geo.upper() for c in o.get('countries', []))]
                    
                    if filtered:
                        df = pd.DataFrame(filtered)
                        st.dataframe(df[['name', 'payout', 'currency', 'status']], use_container_width=True)
                    else:
                        st.warning("No offers found for this GEO.")
                except Exception as e:
                    st.error(f"Link failed: {e}")

# --- ВКЛАДКА 2: УНИКАЛИЗАТОР ---
with tab2:
    st.markdown("### 🛠 High-End Unique Engine")
    up = st.file_uploader("DROP CREATIVE HERE", type=['jpg', 'png'])
    if up:
        img = Image.open(up)
        st.image(img, caption="Original", width=300)
        if st.button("GENERATE 5 BLACK-OPS COPIES"):
            cols = st.columns(5)
            for i in range(5):
                processed = hardcore_unique(img)
                buf = io.BytesIO()
                processed.save(buf, format="JPEG", quality=random.randint(85, 95))
                cols[i].image(processed, use_container_width=True)
                cols[i].download_button(f"GET #{i+1}", buf.getvalue(), f"v_{i+1}.jpg")

# --- ВКЛАДКА 3: АНАЛИТИКА ---
with tab3:
    st.markdown("### 🧮 Profit Margin Calculator")
    c1, c2, c3 = st.columns(3)
    with c1:
        p = st.number_input("Payout ($)", value=20.0)
    with c2:
        cr = st.number_input("Lp CR (%)", value=2.0)
    with c3:
        app = st.number_input("Approve (%)", value=30.0)
    
    be_cpc = calculate_be_cpc(p, cr, app)
    
    st.divider()
    m1, m2 = st.columns(2)
    m1.metric("BREAK-EVEN CPC", f"${round(be_cpc, 3)}")
    m2.metric("TARGET ROI 100% CPC", f"${round(be_cpc/2, 3)}")
    
    if be_cpc < 0.05:
        st.error("⚠️ VERY RISKY ECONOMY: Look for a better offer or improve CR!")
    else:
        st.success("✅ PROFITABLE ZONE: Good potential for scaling.")
