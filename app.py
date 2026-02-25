import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
from PIL import Image
from googletrans import Translator
from engine import hardcore_unique, calculate_be_cpc # Импорт нашей логики

# Инициализация
translator = Translator()
st.set_page_config(page_title="Arbitrage OS v4.0", layout="wide")

# --- ИНТЕРФЕЙС ---
st.title("🛰️ Arbitrage Command Center")

tab1, tab2, tab3 = st.tabs(["🚀 Launch", "🎨 Factory", "📊 Analytics"])

with tab1:
    st.subheader("Localization & Offers")
    geo = st.text_input("Target GEO (e.g. KZ)", "KZ")
    msg = st.text_area("Ad Text (RU)", "Вам одобрена выплата!")
    if st.button("Translate"):
        dest = 'kk' if geo == "KZ" else geo.lower()
        res = translator.translate(msg, dest=dest).text
        st.success(f"Result ({geo}): {res}")

with tab2:
    st.subheader("Deep Unique Engine")
    up = st.file_uploader("Upload Image", type=['jpg', 'png'])
    if up:
        img = Image.open(up)
        if st.button("Generate 5 Variants"):
            cols = st.columns(5)
            for i in range(5):
                processed = hardcore_unique(img)
                buf = io.BytesIO()
                processed.save(buf, format="JPEG", quality=90)
                cols[i].image(processed)
                cols[i].download_button(f"Save {i}", buf.getvalue(), f"v{i}.jpg")

with tab3:
    st.subheader("Unit Economics")
    p = st.number_input("Payout ($)", value=20.0)
    c = st.number_input("CR (%)", value=2.0)
    a = st.number_input("Approve (%)", value=30.0)
    be_cpc = calculate_be_cpc(p, c, a)
    st.metric("Break-even CPC", f"${round(be_cpc, 3)}")