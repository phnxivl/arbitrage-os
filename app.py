# --- ВКЛАДКА 1: ЭКОНОМИКА ---
with t_calc:
    st.subheader("Расчет доходности с конвертацией")
    
    # 1. Сетка ввода
    c1, c2 = st.columns([2, 1])
    
    with c1:
        # В какой валюте выплата в партнерке
        payout_curr = st.selectbox("Валюта выплаты (в партнерке)", ["USD", "EUR", "RUB", "KZT", "UAH"], key="p_curr")
        pay_val = st.number_input(f"Сумма выплаты ({payout_curr})", value=25.0, step=1.0)
        
        st.divider()
        
        # В какой валюте считаем CPC (расход)
        target_curr = st.selectbox("Валюта расхода (закупка трафика)", ["USD", "KZT", "RUB", "UAH", "EUR"], key="t_curr")
        
        # Данные конверсии
        cc1, cc2 = st.columns(2)
        cr = cc1.number_input("CR лендинга (%)", value=2.0, step=0.1)
        app = cc2.number_input("Аппрув (%)", value=40.0, step=1.0)
        
    # 2. ЛОГИКА КОНВЕРТАЦИИ
    # Получаем курсы
    rate_payout = get_rate(payout_curr) # Курс валюты выплаты к USD
    rate_target = get_rate(target_curr) # Курс валюты расхода к USD
    
    # Переводим выплату в USD для расчета
    pay_in_usd = pay_val / rate_payout
    
    # Считаем безубыточный CPC в USD
    be_usd = pay_in_usd * (cr / 100) * (app / 100)
    
    # Переводим итоговый CPC в целевую валюту
    be_local = be_usd * rate_target
    
    with c2:
        st.metric(f"МАКС. CPC ({target_curr})", f"{round(be_local, 3)}")
        st.metric("ROI 100% CPC", f"{round(be_local/2, 3)}")
        
        st.write("---")
        st.write(f"**Курсы валют:**")
        st.caption(f"1 USD = {rate_payout} {payout_curr}")
        st.caption(f"1 USD = {rate_target} {target_curr}")
        
        if payout_curr != target_curr:
            st.info(f"Выплата {pay_val} {payout_curr} ≈ {round(pay_in_usd, 2)} USD")
