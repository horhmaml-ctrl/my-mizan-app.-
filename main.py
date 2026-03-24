import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات النظام ---
st.set_page_config(page_title="الخوارزمي المحاسبي Pro", layout="centered")

# --- محاكاة قاعدة البيانات (المنظمة المحاسبية) ---
if 'db' not in st.session_state:
    st.session_state.db = {
        'journal': pd.DataFrame(columns=['رقم_القيد', 'التاريخ', 'الحساب', 'مدين', 'دائن', 'البيان']),
        'inventory': {'صنف A': 100, 'صنف B': 50},
        'page': 'home'
    }

# --- محرك القيود المزدوجة (The Accounting Engine) ---
def record_transaction(debit_acc, credit_acc, amount, note):
    """وظيفة تضمن توازن النظام المحاسبي 100%"""
    new_id = (len(st.session_state.db['journal']) // 2) + 1
    date = datetime.now().strftime("%Y-%m-%d")
    
    # طرف المدين
    debit_entry = {'رقم_القيد': new_id, 'التاريخ': date, 'الحساب': debit_acc, 'مدين': amount, 'دائن': 0, 'البيان': note}
    # طرف الدائن
    credit_entry = {'رقم_القيد': last_id if 'last_id' in locals() else new_id, 'التاريخ': date, 'الحساب': credit_acc, 'مدين': 0, 'دائن': amount, 'البيان': note}
    
    st.session_state.db['journal'] = pd.concat([st.session_state.db['journal'], pd.DataFrame([debit_entry, credit_entry])], ignore_index=True)

# --- واجهة المستخدم (التصميم الاحترافي) ---
st.markdown("""
    <style>
    .block-container { padding: 0px !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f8fafc; }
    .nav-header { background: #1e3a8a; color: white; padding: 20px; text-align: center; font-weight: bold; font-size: 20px; }
    div.stButton > button { width: 100%; height: 50px; border-radius: 12px; font-weight: bold; }
    .stats-box { background: white; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- التنقل بين الموديلات المحاسبية ---

# 1. لوحة التحكم (الرئيسية)
if st.session_state.db['page'] == 'home':
    st.markdown("<div class='nav-header'>نظام الخوارزمي للمحاسبة والمستودعات</div>", unsafe_allow_html=True)
    
    # حساب الأرصدة لحظياً من دفتر اليومية
    df = st.session_state.db['journal']
    total_sales = df[df['الحساب'] == 'المبيعات']['دائن'].sum()
    cash_balance = df[df['الحساب'] == 'الصندوق']['مدين'].sum() - df[df['الحساب'] == 'الصندوق']['دائن'].sum()

    st.write(" ")
    col1, col2 = st.columns(2)
    with col1: st.markdown(f"<div class='stats-box'>💰 رصيد الصندوق<br><h2>{cash_balance:,.2f}</h2></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='stats-box'>📈 إجمالي المبيعات<br><h2>{total_sales:,.2f}</h2></div>", unsafe_allow_html=True)

    st.write("---")
    # أزرار الوصول السريع (تحاكي الصورة التي أرفقتها)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("➕ فاتورة"): st.session_state.db['page'] = 'invoice'; st.rerun()
    with c2: 
        if st.button("📝 سند صرف"): st.session_state.db['page'] = 'voucher'; st.rerun()
    with c3: 
        if st.button("📊 التقارير"): st.session_state.db['page'] = 'reports'; st.rerun()

# 2. موديل الفواتير (ترابط محاسبي ومخزني)
elif st.session_state.db['page'] == 'invoice':
    st.markdown("<div class='nav-header'>تحرير فاتورة مبيعات</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.db['page'] = 'home'; st.rerun()
    
    with st.form("invoice_form"):
        item = st.selectbox("اختر الصنف", list(st.session_state.db['inventory'].keys()))
        qty = st.number_input("الكمية", min_value=1)
        price = st.number_input("السعر", value=10.0)
        
        if st.form_submit_button("ترحيل وحفظ الفاتورة"):
            total = qty * price
            # إجراء القيد المزدوج تلقائياً (من الصندوق إلى المبيعات)
            record_transaction("الصندوق", "المبيعات", total, f"بيع {qty} من {item}")
            # تحديث المخزن فوراً
            st.session_state.db['inventory'][item] -= qty
            st.success(f"تم الحفظ! إجمالي الفاتورة: {total}")

# 3. موديل التقارير (دفتر الأستاذ وميزان المراجعة)
elif st.session_state.db['page'] == 'reports':
    st.markdown("<div class='nav-header'>التقارير المالية الختامية</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.db['page'] = 'home'; st.rerun()
    
    st.subheader("📖 دفتر اليومية العام")
    st.dataframe(st.session_state.db['journal'], use_container_width=True)
    
    st.write("---")
    st.subheader("⚖️ ميزان المراجعة بالأرصدة")
    trial_balance = st.session_state.db['journal'].groupby('الحساب')[['مدين', 'دائن']].sum()
    st.table(trial_balance)
