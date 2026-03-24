import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات النظام المحاسبي ---
st.set_page_config(page_title="نظام الخوارزمي المحاسبي Pro", layout="wide")

# --- محاكاة قاعدة البيانات (Database Engine) ---
if 'db' not in st.session_state:
    st.session_state.db = {
        'journal': pd.DataFrame(columns=['id', 'date', 'account', 'debit', 'credit', 'ref', 'note']),
        'accounts': {
            '101': {'name': 'الصندوق الرئيسي', 'type': 'Assets'},
            '102': {'name': 'المخزن العام', 'type': 'Assets'},
            '201': {'name': 'الموردين', 'type': 'Liabilities'},
            '301': {'name': 'المبيعات', 'type': 'Revenue'},
            '401': {'name': 'المصاريف العمومية', 'type': 'Expenses'}
        },
        'inventory': {'صنف A': {'qty': 100, 'cost': 50}, 'صنف B': {'qty': 200, 'cost': 30}}
    }

# --- المحرك المحاسبي (Accounting Core) ---
def add_journal_entry(date, entries, ref, note):
    # التأكد من توازن القيد (المدين = الدائن)
    total_debit = sum([e['debit'] for e in entries])
    total_credit = sum([e['credit'] for e in entries])
    
    if total_debit != total_credit:
        return False, "القيد غير متوازن!"
    
    new_id = len(st.session_state.db['journal']) + 1
    for e in entries:
        row = {
            'id': new_id, 'date': date, 'account': e['acc'],
            'debit': e['debit'], 'credit': e['credit'],
            'ref': ref, 'note': note
        }
        st.session_state.db['journal'] = pd.concat([st.session_state.db['journal'], pd.DataFrame([row])], ignore_index=True)
    return True, "تم الترحيل بنجاح"

# --- الواجهة البرمجية للجوال ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .main-header { background: #1a365d; color: white; padding: 20px; text-align: center; border-radius: 0 0 20px 20px; margin-bottom: 20px; }
    .card { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (نظام الموديلات) ---
menu = st.sidebar.radio("القائمة الرئيسية", ["لوحة التحكم", "فاتورة مبيعات", "سند صرف", "دفتر الأستاذ", "المخازن"])

# --- 1. لوحة التحكم (الملخص المالي) ---
if menu == "لوحة التحكم":
    st.markdown("<div class='main-header'><h1>الخوارزمي المحاسبي </h1></div>", unsafe_allow_html=True)
    
    # حساب الأرصدة لحظياً من دفتر اليومية
    df = st.session_state.db['journal']
    revenue = df[df['account'] == '301']['credit'].sum()
    expenses = df[df['account'] == '401']['debit'].sum()
    cash = df[df['account'] == '101']['debit'].sum() - df[df['account'] == '101']['credit'].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("المبيعات (إيراد)", f"{revenue:,.2f}")
    c2.metric("المصاريف", f"{expenses:,.2f}")
    c3.metric("رصيد الصندوق", f"{cash:,.2f}")

# --- 2. فاتورة مبيعات (ترابط محاسبي) ---
elif menu == "فاتورة مبيعات":
    st.header("📝 فاتورة مبيعات جديدة")
    with st.form("sale_form"):
        item = st.selectbox("اختر الصنف", list(st.session_state.db['inventory'].keys()))
        qty = st.number_input("الكمية", min_value=1)
        price = st.number_input("سعر البيع", min_value=1.0)
        
        if st.form_submit_button("حفظ وترحيل"):
            total = qty * price
            # إنشاء القيد المزدوج تلقائياً
            entries = [
                {'acc': '101', 'debit': total, 'credit': 0}, # المدين: الصندوق
                {'acc': '301', 'debit': 0, 'credit': total}  # الدائن: المبيعات
            ]
            success, msg = add_journal_entry(datetime.now().date(), entries, "INV-100", f"بيع {qty} من {item}")
            if success:
                st.session_state.db['inventory'][item]['qty'] -= qty
                st.success(msg)

# --- 3. دفتر الأستاذ (الشفافية المالية) ---
elif menu == "دفتر الأستاذ":
    st.header("📖 دفتر اليومية العام")
    st.dataframe(st.session_state.db['journal'], use_container_width=True)

    st.write("---")
    st.header("⚖️ ميزان المراجعة")
    ledger = st.session_state.db['journal'].groupby('account').agg({'debit':'sum', 'credit':'sum'})
    st.table(ledger)
