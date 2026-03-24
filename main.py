import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات البرنامج الأساسية
st.set_page_config(page_title="برنامج الخوارزمي المحاسبي", layout="centered")

# --- محاكي قاعدة البيانات (Storage) ---
if 'transactions' not in st.session_state:
    st.session_state.transactions = [] # لتخزين القيود المحاسبية
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- تصميم الواجهة (CSS) ليكون احترافياً وهادئاً ---
st.markdown("""
    <style>
    .block-container { padding: 0px !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f4f7f6; }
    .main-title { background: #2c3e50; color: white; padding: 20px; text-align: center; font-size: 22px; font-weight: bold; border-radius: 0 0 20px 20px; }
    .stat-card { background: white; padding: 15px; border-radius: 10px; border-right: 5px solid #27ae60; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- الوظائف المحاسبية (The Logic) ---
def save_invoice(customer, amount):
    # توليد قيد محاسبي آلي
    entry = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "البيان": f"مبيعات لـ {customer}",
        "مدين (صندوق)": amount,
        "دائن (مبيعات)": amount
    }
    st.session_state.transactions.append(entry)

# --- عرض الصفحات ---

# 1. لوحة التحكم (الرئيسية)
if st.session_state.page == 'dashboard':
    st.markdown("<div class='main-title'>الخوارزمي للمحاسبة الذكية</div>", unsafe_allow_html=True)
    
    # عرض ملخص مالي سريع
    total_sales = sum([t['دائن (مبيعات)'] for t in st.session_state.transactions])
    
    st.write(" ")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='stat-card'><p>إجمالي المبيعات</p><h3>{total_sales:,.2f}</h3></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-card' style='border-right-color:#e74c3c'><p>عدد العمليات</p><h3>{len(st.session_state.transactions)}</h3></div>", unsafe_allow_html=True)

    st.write("---")
    
    # أزرار العمليات
    if st.button("➕ فاتورة بيع جديدة", use_container_width=True):
        st.session_state.page = 'invoice'
        st.rerun()
        
    if st.button("📑 كشف الحساب العام", use_container_width=True):
        st.session_state.page = 'report'
        st.rerun()

# 2. صفحة الفاتورة (الإدخال)
elif st.session_state.page == 'invoice':
    st.markdown("<div class='main-title'>تحرير فاتورة بيع</div>", unsafe_allow_html=True)
    
    with st.form("inv_form"):
        cust_name = st.text_input("اسم العميل", "عميل نقدي")
        inv_amount = st.number_input("إجمالي المبلغ", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("حفظ وترحيل الفاتورة")
        
        if submitted:
            save_invoice(cust_name, inv_amount)
            st.success("تم ترحيل الفاتورة للحسابات بنجاح!")
            
    if st.button("🔙 العودة للرئيسية"):
        st.session_state.page = 'dashboard'
        st.rerun()

# 3. صفحة التقارير (كشف الحساب)
elif st.session_state.page == 'report':
    st.markdown("<div class='main-title'>كشف الحساب الختامي</div>", unsafe_allow_html=True)
    
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        st.table(df) # عرض القيود المحاسبية كما هي في الدفاتر
    else:
        st.warning("لا توجد عمليات مسجلة بعد.")
        
    if st.button("🔙 عودة"):
        st.session_state.page = 'dashboard'
        st.rerun()
