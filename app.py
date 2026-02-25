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
    [data-testid="stMetricValue"] { color: #00FF41 !important; text-shadow: 0 0 10px rgba(0,255,65,0.4); }
    .stButton>button { background: linear-gradient(45deg, #0052D4, #4364F7); border: none; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Функции
def get_rate(c):
    try:
        r = httpx.get(f"https://open.er-api.com/v6/latest/USD", timeout=2)
        return r.json()['rates'].get(c, 1.0)
    except: return 1.0

def process_batch(img, count=5):
    res = []
    for _ in range(count):
        temp = img.rotate(random.uniform(-2, 2))
        if random.choice([True, False]): temp = ImageOps.mirror(temp)
        res
