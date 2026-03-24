import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. الإعدادات الهيكلية للنظام (الخوارزمي برو) ---
st.set_page_config(page_title="الخوارزمي للمحاسبة والمستودعات", layout="wide")

# --- 2. محرك قاعدة البيانات والذاكرة المركزية ---
if 'db' not in st.session_state:
    st.session_state.db = {
        # دفتر اليومية العام (الأصل في كل البرامج المحاسبية)
        'journal': pd.DataFrame(columns=['رقم_القيد', 'التاريخ', 'الحساب', 'البيان', 'مدين', 'دائن']),
        # شجرة الحسابات (الأرصدة الافتتاحية كما في صورتك)
        'accounts': {
            '101': {'name': 'الصندوق الرئيسي', 'balance': 380500.00, 'type': 'Asset'},
            '102': {'name': 'صرافة السنيري', 'balance': 13068955.00, 'type': 'Asset'},
            '301': {'name': 'إيراد المبيعات', 'balance': 0.00, 'type': 'Revenue'},
            '401': {'name': 'تكلفة البضاعة', 'balance': 0.00, 'type': 'Expense'}
        },
        # المستودعات (الأصناف والكميات)
        'warehouse': {
            'صنف A': {'qty': 100, 'cost': 50, 'price': 75},
            'صنف B': {'qty': 200, 'cost': 120, 'price': 150}
        }
    }

# --- 3. المحرك المحاسبي المركزي (Core Accounting Engine) ---
def post_to_ledger(debit_acc_code, credit_acc_code, amount, note, item=None, qty=0):
    """وظيفة الترحيل الآلي لضمان توازن الميزانية"""
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry_id = len(st.session_state.db['journal']) // 2 + 1
    
    # تحديث أرصدة الحسابات
    st.session_state.db['accounts'][debit_acc_code]['balance'] += amount
    st.session_state.db['accounts'][credit_acc_code]['balance'] += amount # دائن يزيد في المبيعات
    
    # تحديث المخزن إذا وجدت حركة أصناف
    if item and qty > 0:
        st.session_state.db['warehouse'][item]['qty'] -= qty

    # تسجيل القيد المزدوج (المدين والدائن)
    d_name = st.session_state.db['accounts'][debit_acc_code]['name']
    c_name = st.session_state.db['accounts'][credit_acc_code]['name']
    
    new_entries = [
        {'رقم_القيد': entry_id, 'التاريخ': date, 'الحساب': d_name, 'البيان': note, 'مدين': amount, 'دائن': 0},
        {'رقم_القيد': entry_id, 'التاريخ': date, 'الحساب': c_name, 'البيان': note, 'مدين': 0, 'دائن': amount}
    ]
    st.session_state.db['journal'] = pd.concat([st.session_state.db['journal'], pd.DataFrame(new_entries)], ignore_index=True)

# --- 4. واجهة المستخدم (تصميم الميزان دوت نت) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-header { background: #1e3a8a; color: white; padding: 20px; text-align: center; border-radius: 0 0 20px 20px; margin-bottom: 20px; }
    .mizan-card { background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .sidebar-title { color: #1e3a8a; font-weight: bold; font-size: 18px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>نظام الخوارزمي دوت نت 2026</h1><p>للمحاسبة والمستودعات المتكاملة</p></div>", unsafe_allow_html=True)

# القائمة الجانبية (الأيقونات الوظيفية)
menu = st.sidebar.radio("📁 القائمة البرمجية", ["لوحة التحكم (الرئيسية)", "فاتورة مبيعات", "كشف حساب تفصيلي", "جرد المستودع"])

# --- موديول: لوحة التحكم ---
if menu == "لوحة التحكم (الرئيسية)":
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(f"💰 الصندوق الرئيسي\n\n {st.session_state.db['accounts']['101']['balance']:,.2f}")
    with c2:
        st.success(f"🏦 صرافة السنيري\n\n {st.session_state.db['accounts']['102']['balance']:,.2f}")
    with c3:
        st.warning(f"📉 إجمالي الإيرادات\n\n {st.session_state.db['accounts']['301']['balance']:,.2f}")
    
    st.write("---")
    st.subheader("📊 القيود اليومية الأخيرة")
    st.dataframe(st.session_state.db['journal'].tail(10), use_container_width=True)

# --- موديول: فاتورة مبيعات (الربط المحاسبي) ---
elif menu == "فاتورة مبيعات":
    st.header("📝 تحرير فاتورة مبيعات جديدة")
    with st.form("invoice_form"):
        col_x, col_y = st.columns(2)
        item = col_x.selectbox("اختر الصنف من المخزن", list(st.session_state.db['warehouse'].keys()))
        acc = col_y.selectbox("حساب التحصيل (مدين)", ['101', '102'], format_func=lambda x: st.session_state.db['accounts'][x]['name'])
        qty = col_x.number_input("الكمية المباعة", min_value=1)
        price = st.session_state.db['warehouse'][item]['price']
        total = qty * price
        st.markdown(f"### الإجمالي النهائي: **{total:,.2f} ريال**")
        
        if st.form_submit_button("حفظ وترحيل الفاتورة ✅"):
            post_to_ledger(acc, '301', total, f"مبيعات صنف: {item}", item, qty)
            st.success("تم الحفظ! تم تحديث المخزن والأرصدة ودفتر اليومية بنجاح.")

# --- موديول: كشف الحساب (التقارير) ---
elif menu == "كشف حساب تفصيلي":
    st.header("🔍 استعلام عن حركة حساب")
    target_acc = st.selectbox("اختر الحساب", ['101', '102', '301'], format_func=lambda x: st.session_state.db['accounts'][x]['name'])
    acc_name = st.session_state.db['accounts'][target_acc]['name']
    
    report_df = st.session_state.db['journal'][st.session_state.db['journal']['الحساب'] == acc_name].copy()
    if not report_df.empty:
        report_df['الرصيد التراكمي'] = report_df['مدين'].cumsum() - report_df['دائن'].cumsum()
        st.table(report_df)
    else:
        st.warning("لا توجد حركات مسجلة لهذا الحساب حالياً.")

# --- موديول: المخازن ---
elif menu == "جرد المستودع":
    st.header("📦 حالة المخزون الحالي")
    inventory_df = pd.DataFrame(st.session_state.db['warehouse']).T
    st.table(inventory_df)
