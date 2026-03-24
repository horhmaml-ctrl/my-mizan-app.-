import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات النظام الكبرى ---
st.set_page_config(page_title="الخوارزمي - النظام المحاسبي المتكامل", layout="wide")

# --- محاكي المحرك المالي (Financial Engine) ---
if 'khwarizmi_core' not in st.session_state:
    st.session_state.khwarizmi_core = {
        'journal': pd.DataFrame(columns=['رقم_القيد', 'التاريخ', 'الحساب', 'البيان', 'مدين', 'دائن', 'الرصيد_التراكمي']),
        'warehouse': {'صنف ممتاز': {'الكمية': 100, 'التكلفة': 50, 'السعر': 85}, 'صنف عادي': {'الكمية': 200, 'التكلفة': 20, 'السعر': 40}},
        'accounts': {'101': 'الصندوق الرئيسي', '102': 'صرافة السنيري', '301': 'إيراد المبيعات', '401': 'تكلفة البضاعة'},
        'balances': {'101': 380500.0, '102': 13068955.0, '301': 0.0, '401': 0.0}
    }

# --- وظيفة الترحيل الآلي (Posting Logic) ---
def execute_transaction(debit_acc, credit_acc, amount, note, item_name=None, qty=0):
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    txn_id = len(st.session_state.khwarizmi_core['journal']) // 2 + 1
    
    # 1. تحديث الأرصدة في الدليل
    st.session_state.khwarizmi_core['balances'][debit_acc] += amount
    st.session_state.khwarizmi_core['balances'][credit_acc] += amount # للمبيعات تزيد كدائن في المنطق البرمجي

    # 2. تحديث المخازن
    if item_name and qty > 0:
        st.session_state.khwarizmi_core['warehouse'][item_name]['الكمية'] -= qty

    # 3. تسجيل القيد المزدوج في دفتر اليومية
    entries = [
        {'رقم_القيد': txn_id, 'التاريخ': date, 'الحساب': st.session_state.khwarizmi_core['accounts'][debit_acc], 'البيان': note, 'مدين': amount, 'دائن': 0},
        {'رقم_القيد': txn_id, 'التاريخ': date, 'الحساب': st.session_state.khwarizmi_core['accounts'][credit_acc], 'البيان': note, 'مدين': 0, 'دائن': amount}
    ]
    st.session_state.khwarizmi_core['journal'] = pd.concat([st.session_state.khwarizmi_core['journal'], pd.DataFrame(entries)], ignore_index=True)

# --- واجهة البرنامج (تصميم الميزان دوت نت) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .mizan-header { background: linear-gradient(90deg, #2c3e50, #34495e); color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; }
    .card { background: white; padding: 15px; border: 1px solid #d1d5db; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='mizan-header'>نظام الخوارزمي - لإدارة الحسابات والمستودعات</div>", unsafe_allow_html=True)

# القائمة الرئيسية
tab1, tab2, tab3, tab4 = st.tabs(["🏠 الرئيسية", "🛒 الفواتير", "📊 التقارير المالية", "📦 المخازن"])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 الصندوق الرئيسي", f"{st.session_state.khwarizmi_core['balances']['101']:,.2f}")
    c2.metric("🏦 صرافة السنيري", f"{st.session_state.khwarizmi_core['balances']['102']:,.2f}")
    c3.metric("📈 إجمالي المبيعات", f"{st.session_state.khwarizmi_core['balances']['301']:,.2f}")

with tab2:
    st.subheader("تحرير فاتورة مبيعات")
    with st.form("sale_form"):
        col1, col2 = st.columns(2)
        item = col1.selectbox("الصنف", list(st.session_state.khwarizmi_core['warehouse'].keys()))
        acc = col2.selectbox("الترحيل إلى", ['101', '102'], format_func=lambda x: st.session_state.khwarizmi_core['accounts'][x])
        qty = col1.number_input("الكمية", min_value=1)
        price = st.session_state.khwarizmi_core['warehouse'][item]['السعر']
        st.write(f"**سعر الوحدة:** {price} | **الإجمالي:** {qty*price}")
        
        if st.form_submit_button("حفظ وترحيل"):
            execute_transaction(acc, '301', qty*price, f"مبيعات {item}", item, qty)
            st.success("تم الحفظ والترحيل للمخازن والحسابات!")

with tab3:
    st.subheader("دفتر اليومية العام (القيود المترابطة)")
    st.table(st.session_state.khwarizmi_core['journal'])

with tab4:
    st.subheader("جرد المستودعات")
    st.dataframe(pd.DataFrame(st.session_state.khwarizmi_core['warehouse']).T)
