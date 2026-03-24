import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات النظام ---
st.set_page_config(page_title="نظام الخوارزمي المحاسبي", layout="centered")

# --- محاكي قاعدة البيانات المحاسبية ---
if 'ledger' not in st.session_state:
    # دفتر الأستاذ العام (التاريخ، الحساب، مدين، دائن، البيان)
    st.session_state.ledger = pd.DataFrame(columns=['التاريخ', 'الحساب', 'مدين', 'دائن', 'البيان'])
if 'inventory' not in st.session_state:
    # المخزن (الصنف، الكمية، سعر التكلفة)
    st.session_state.inventory = {"صنف 1": 100, "صنف 2": 50}
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- وظائف المحرك المحاسبي ---
def post_transaction(date, debit_acc, credit_acc, amount, note):
    """وظيفة الترحيل الآلي للقيود المزدوجة"""
    new_entries = [
        {'التاريخ': date, 'الحساب': debit_acc, 'مدين': amount, 'دائن': 0, 'البيان': note},
        {'التاريخ': date, 'الحساب': credit_acc, 'مدين': 0, 'دائن': amount, 'البيان': note}
    ]
    st.session_state.ledger = pd.concat([st.session_state.ledger, pd.DataFrame(new_entries)], ignore_index=True)

# --- واجهة المستخدم (CSS) ---
st.markdown("""
    <style>
    .block-container { padding: 0px !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f8fafc; }
    .header-box { background: linear-gradient(90deg, #1e3a8a, #2563eb); color: white; padding: 20px; text-align: center; border-radius: 0 0 20px 20px; }
    .footer-fixed { position: fixed; bottom: 0; width: 100%; background: #1e3a8a; color: white; display: grid; grid-template-columns: 1fr 1fr 1fr; text-align: center; padding: 10px 0; font-size: 12px; }
    div.stButton > button { width: 100%; height: 50px; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- التنقل بين الصفحات ---

# 1. لوحة التحكم الرئيسية
if st.session_state.page == 'home':
    st.markdown("<div class='header-box'><h2>الخوارزمي للمحاسبة</h2><p>نظام إدارة الأنشطة التجارية</p></div>", unsafe_allow_html=True)
    
    # حساب الإجماليات من دفتر الأستاذ
    total_revenue = st.session_state.ledger[st.session_state.ledger['الحساب'] == 'المبيعات']['دائن'].sum()
    total_expenses = st.session_state.ledger[st.session_state.ledger['الحساب'] == 'المصاريف']['مدين'].sum()
    net_profit = total_revenue - total_expenses

    st.write(" ")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"💰 الإيرادات\n\n {total_revenue:,.2f}")
    with col2:
        st.warning(f"📉 المصاريف\n\n {total_expenses:,.2f}")

    st.write("---")
    
    # شبكة العمليات
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("➕ فاتورة"): st.session_state.page = 'sales'; st.rerun()
    with c2: 
        if st.button("💸 صرف"): st.session_state.page = 'expense'; st.rerun()
    with c3: 
        if st.button("📊 تقارير"): st.session_state.page = 'reports'; st.rerun()

    st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='footer-fixed'><div>الإيرادات<br>{total_revenue}</div><div>المصاريف<br>{total_expenses}</div><div>الأرباح<br>{net_profit}</div></div>", unsafe_allow_html=True)

# 2. صفحة فاتورة المبيعات (المحاكاة الكاملة)
elif st.session_state.page == 'sales':
    st.markdown("<div class='header-box'><h3>تحرير فاتورة مبيعات</h3></div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = 'home'; st.rerun()
    
    with st.form("sales_form"):
        customer = st.selectbox("العميل", ["عميل نقدي", "شركة الأمل", "مؤسسة النجاح"])
        item = st.selectbox("الصنف", list(st.session_state.inventory.keys()))
        qty = st.number_input("الكمية", min_value=1, value=1)
        price = st.number_input("سعر الوحدة", min_value=0.0, value=100.0)
        total = qty * price
        st.write(f"### الإجمالي: {total:,.2f}")
        
        if st.form_submit_button("ترحيل وحفظ الفاتورة ✅"):
            # 1. القيد المحاسبي (من الصندوق إلى المبيعات)
            post_transaction(datetime.now().date(), "الصندوق الرئيسي", "المبيعات", total, f"فاتورة مبيعات - {customer}")
            # 2. حركة المخزن (خصم الكمية)
            st.session_state.inventory[item] -= qty
            st.success("تم ترحيل الفاتورة وتحديث المخزن والحسابات!")

# 3. صفحة التقارير والقيود
elif st.session_state.page == 'reports':
    st.markdown("<div class='header-box'><h3>دفتر اليومية العام</h3></div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.page = 'home'; st.rerun()
    
    if not st.session_state.ledger.empty:
        st.dataframe(st.session_state.ledger, use_container_width=True)
        
        # ميزان المراجعة المصغر
        st.write("---")
        st.subheader("ميزان مراجعة سريع")
        trial_balance = st.session_state.ledger.groupby('الحساب')[['مدين', 'دائن']].sum()
        st.table(trial_balance)
    else:
        st.info("لا توجد قيود محاسبية مسجلة حالياً.")
