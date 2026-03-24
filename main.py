import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. الإعدادات الهيكلية لنظام الخوارزمي ---
st.set_page_config(page_title="الخوارزمي - نظام محاسبي متكامل", layout="wide")

if 'khwarizmi_db' not in st.session_state:
    st.session_state.khwarizmi_db = {
        'journal': pd.DataFrame(columns=['رقم', 'التاريخ', 'الحساب', 'البيان', 'مدين', 'دائن', 'الرصيد']),
        'inventory': {'صنف ممتاز': {'qty': 150, 'cost': 500, 'price': 650}, 'صنف عادي': {'qty': 300, 'cost': 100, 'price': 150}},
        'accounts': {
            '101': {'name': 'الصندوق الرئيسي', 'bal': 380500.00, 'type': 'Asset'},
            '102': {'name': 'صرافة السنيري', 'bal': 13068955.00, 'type': 'Asset'},
            '301': {'name': 'المبيعات', 'bal': 0.00, 'type': 'Revenue'},
            '401': {'name': 'المصاريف', 'bal': 0.00, 'type': 'Expense'}
        },
        'page': 'dashboard'
    }

# --- 2. محرك العمليات (Logic Engine) محاكاة للميزان دوت نت ---
def post_transaction(acc_debit, acc_credit, amount, note, item=None, qty=0):
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    txn_id = len(st.session_state.khwarizmi_db['journal']) // 2 + 1
    
    # تحديث الأرصدة في دليل الحسابات
    if acc_debit in st.session_state.khwarizmi_db['accounts']:
        st.session_state.khwarizmi_db['accounts'][acc_debit]['bal'] += amount
    if acc_credit in st.session_state.khwarizmi_db['accounts']:
        st.session_state.khwarizmi_db['accounts'][acc_credit]['bal'] += amount # للمبيعات تزيد كدائن

    # تحديث المخزن إذا كانت فاتورة
    if item and qty > 0:
        st.session_state.khwarizmi_db['inventory'][item]['qty'] -= qty

    # تسجيل القيد المزدوج
    d_entry = {'رقم': txn_id, 'التاريخ': date, 'الحساب': acc_debit, 'البيان': note, 'مدين': amount, 'دائن': 0}
    c_entry = {'رقم': txn_id, 'التاريخ': date, 'الحساب': acc_credit, 'البيان': note, 'مدين': 0, 'دائن': amount}
    
    st.session_state.khwarizmi_db['journal'] = pd.concat([
        st.session_state.khwarizmi_db['journal'], pd.DataFrame([d_entry, c_entry])
    ], ignore_index=True)

# --- 3. الواجهة الرسومية (UI) المستوحاة من الأنظمة المتكاملة ---
st.markdown("""
    <style>
    .stApp { background-color: #f1f5f9; }
    .top-bar { background: #1e3a8a; color: white; padding: 15px; text-align: center; border-radius: 0 0 15px 15px; font-size: 24px; font-weight: bold; }
    .mizan-box { background: white; border: 1px solid #cbd5e1; border-radius: 8px; padding: 15px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .mizan-title { background: #334155; color: white; padding: 5px 12px; border-radius: 4px; font-size: 14px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='top-bar'>نظام الخوارزمي للمحاسبة والمستودعات - PRO</div>", unsafe_allow_html=True)

# القائمة الجانبية للتنقل الاحترافي
menu = st.sidebar.radio("📋 القائمة الرئيسية", ["لوحة التحكم", "فاتورة مبيعات", "سندات القيود", "كشوفات الحسابات", "المخازن والجرد"])

# --- موديول 1: لوحة التحكم (الرئيسية كما في الميزان) ---
if menu == "لوحة التحكم":
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("<div class='mizan-box'><div class='mizan-title'>⚠️ تنبيهات النظام</div>آخر نسخة احتياطية: ناجحة<br>تاريخ اليوم: " + datetime.now().strftime("%Y-%m-%d") + "</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='mizan-box'><div class='mizan-title'>🔗 اختصارات سريعة</div>", unsafe_allow_html=True)
        if st.button("تحرير فاتورة"): pass
        if st.button("كشف حساب"): pass
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='mizan-box'><div class='mizan-title'>🏦 أرصدة الصناديق</div>", unsafe_allow_html=True)
        for code, acc in st.session_state.khwarizmi_db['accounts'].items():
            if acc['type'] == 'Asset': st.write(f"**{acc['name']}:** {acc['bal']:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

# --- موديول 2: فاتورة المبيعات ---
elif menu == "فاتورة مبيعات":
    st.header("🛒 نظام الفواتير المتكامل")
    with st.form("sale_inv"):
        c1, c2 = st.columns(2)
        item = c1.selectbox("الصنف", list(st.session_state.khwarizmi_db['inventory'].keys()))
        acc = c2.selectbox("الحساب المتأثر", ["101", "102"], format_func=lambda x: st.session_state.khwarizmi_db['accounts'][x]['name'])
        qty = c1.number_input("الكمية", min_value=1)
        price = st.session_state.khwarizmi_db['inventory'][item]['price']
        st.info(f"إجمالي قيمة الفاتورة: {qty * price:,.2f}")
        
        if st.form_submit_button("حفظ وترحيل الفاتورة ✅"):
            post_transaction(acc, '301', qty*price, f"فاتورة مبيعات صنف {item}", item, qty)
            st.success("تم الحفظ وتحديث المخزن والحسابات فوراً")

# --- موديول 3: كشوفات الحسابات ---
elif menu == "كشوفات الحسابات":
    st.header("🔍 كشف حساب تفصيلي")
    target = st.selectbox("اختر الحساب", list(st.session_state.khwarizmi_db['accounts'].keys()), format_func=lambda x: st.session_state.khwarizmi_db['accounts'][x]['name'])
    df = st.session_state.khwarizmi_db['journal']
    # منطق التصفية وحساب الرصيد المتحرك
    filtered = df[df['الحساب'].str.contains(target) if target == '101' else df['الحساب'] == st.session_state.khwarizmi_db['accounts'][target]['name']]
    st.table(filtered)

# --- موديول 4: المخازن ---
elif menu == "المخازن والجرد":
    st.header("📦 جرد المستودعات")
    st.table(pd.DataFrame(st.session_state.khwarizmi_db['inventory']).T)
