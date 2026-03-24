import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات النظام ---
st.set_page_config(page_title="الخوارزمي المحاسبي Pro", layout="centered")

# --- محاكي قاعدة البيانات (المنظمة المحاسبية) ---
if 'data' not in st.session_state:
    st.session_state.data = {
        'journal': pd.DataFrame(columns=['رقم_القيد', 'التاريخ', 'الحساب', 'مدين', 'دائن', 'البيان']),
        'inventory': {'صنف ممتاز': {'qty': 100, 'price': 50}, 'صنف عادي': {'qty': 200, 'price': 30}},
        'accounts': {'101': 'الصندوق', '102': 'المخزن', '301': 'المبيعات', '401': 'المصاريف'},
        'page': 'home'
    }

# --- تنسيق الواجهة (محاكاة الأندرويد المحاسبي) ---
st.markdown("""
    <style>
    .block-container { padding: 0px !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f1f5f9; }
    .app-bar { background: #1e3a8a; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 20px; }
    .card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 15px; }
    .mizan-card { background: white; border-radius: 12px; padding: 20px; text-align: center; border: 1px solid #cbd5e1; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .footer-bar { position: fixed; bottom: 0; width: 100%; background: #1e3a8a; color: white; display: grid; grid-template-columns: 1fr 1fr 1fr; text-align: center; padding: 10px 0; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك العمليات (Logic) ---
def post_entry(acc_debit, acc_credit, amount, note):
    # نظام القيد المزدوج: يؤثر في حسابين في آن واحد لضمان التوازن
    last_id = len(st.session_state.data['journal']) // 2 + 1
    date = datetime.now().strftime("%Y-%m-%d")
    
    entry_debit = {'رقم_القيد': last_id, 'التاريخ': date, 'الحساب': acc_debit, 'مدين': amount, 'دائن': 0, 'البيان': note}
    entry_credit = {'رقم_القيد': last_id, 'التاريخ': date, 'الحساب': acc_credit, 'مدين': 0, 'دائن': amount, 'البيان': note}
    
    st.session_state.data['journal'] = pd.concat([st.session_state.data['journal'], pd.DataFrame([entry_debit, entry_credit])], ignore_index=True)

# --- صفحات التطبيق ---

# 1. الصفحة الرئيسية (واجهة المربعات)
if st.session_state.data['page'] == 'home':
    st.markdown("<div class='app-bar'>نظام الخوارزمي المحاسبي</div>", unsafe_allow_html=True)
    
    # شبكة العمليات السريعة (3 أعمدة)
    col1, col2, col3 = st.columns(3)
    with col1: 
        if st.button("➕ فاتورة"): st.session_state.data['page'] = 'sales'; st.rerun()
    with col2: 
        if st.button("💸 صرف"): st.session_state.data['page'] = 'expense'; st.rerun()
    with col3: 
        if st.button("📖 الأستاذ"): st.session_state.data['page'] = 'ledger'; st.rerun()

    # شبكة البطاقات الرئيسية (2 أعمدة)
    st.write("---")
    c_left, c_right = st.columns(2)
    with c_right:
        st.markdown("<div class='mizan-card'>👤<br>العملاء<br><span style='color:red'>0</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='mizan-card'>📈<br>المبيعات<br><span style='color:red'>0</span></div>", unsafe_allow_html=True)
    with c_left:
        st.markdown("<div class='mizan-card'>🚚<br>الموردين<br><span style='color:red'>0</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='mizan-card'>🏦<br>الصناديق<br><span style='color:red'>1</span></div>", unsafe_allow_html=True)

    # الفوتر السفلي (الإجماليات لحظياً)
    sales_total = st.session_state.data['journal'][st.session_state.data['journal']['الحساب'] == '301 المبيعات']['دائن'].sum()
    st.markdown(f"<div class='footer-bar'><div>الإيرادات<br>{sales_total}</div><div>المصروفات<br>0</div><div>الأرباح<br>{sales_total}</div></div>", unsafe_allow_html=True)

# 2. صفحة فاتورة المبيعات (الترابط المحاسبي)
elif st.session_state.data['page'] == 'sales':
    st.markdown("<div class='app-bar'>تحرير فاتورة مبيعات</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.data['page'] = 'home'; st.rerun()
    
    with st.form("sale"):
        item = st.selectbox("الصنف", list(st.session_state.data['inventory'].keys()))
        qty = st.number_input("الكمية", min_value=1)
        price = st.number_input("السعر", value=100.0)
        if st.form_submit_button("ترحيل الفاتورة ✅"):
            total = qty * price
            # الترحيل المحاسبي (من الصندوق إلى المبيعات)
            post_entry("101 الصندوق", "301 المبيعات", total, f"بيع {qty} من {item}")
            # تحديث المخزن
            st.session_state.data['inventory'][item]['qty'] -= qty
            st.success("تم الترحيل للحسابات والمخازن!")

# 3. صفحة دفتر الأستاذ (التقارير)
elif st.session_state.data['page'] == 'ledger':
    st.markdown("<div class='app-bar'>دفتر اليومية والقيود</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.data['page'] = 'home'; st.rerun()
    
    st.dataframe(st.session_state.data['journal'], use_container_width=True)
    
    st.write("---")
    st.subheader("ميزان المراجعة (الأرصدة)")
    trial = st.session_state.data['journal'].groupby('الحساب')[['مدين', 'دائن']].sum()
    st.table(trial)
