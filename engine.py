import numpy as np
import random
from PIL import Image, ImageEnhance, ImageFilter

def hardcore_unique(img):
    """Профессиональная уникализация для обхода фильтров"""
    # 1. Удаление метаданных через пересборку
    data = list(img.getdata())
    img_clean = Image.new(img.mode, img.size)
    img_clean.putdata(data)
    
    # 2. Микро-зум и кроп (1-2%)
    w, h = img_clean.size
    zoom = random.uniform(0.01, 0.02)
    img_clean = img_clean.crop((w*zoom, h*zoom, w*(1-zoom), h*(1-zoom))).resize((w, h))
    
    # 3. Инъекция шума в синий канал (незаметно для глаза, критично для хеша)
    img_array = np.array(img_clean).astype(np.float16)
    noise = np.random.normal(0, 0.8, (h, w))
    img_array[:, :, 2] += noise 
    
    return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

def calculate_be_cpc(payout, cr, approve):
    """Расчет точки безубыточности"""
    return payout * (cr/100) * (approve/100)