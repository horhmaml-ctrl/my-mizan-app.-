import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. إعدادات النظام المحاسبي ---
st.set_page_config(page_title="الخوارزمي للمحاسبة والمستودعات", layout="wide")

# --- 2. محاكاة قاعدة البيانات (Database Engine) ---
if 'accounting_system' not in st.session_state:
    st.session_state.accounting_system = {
        # دفتر اليومية العام
        'journal': pd.DataFrame(columns=['ID', 'Date', 'Account_Code', 'Account_Name', 'Debit', 'Credit', 'Note']),
        # دليل الحسابات (شجرة الحسابات)
        'chart_of_accounts': {
            '101': {'name': 'الصندوق', 'type': 'Asset', 'balance': 0},
            '102': {'name': 'المخزن الرئيسي', 'type': 'Asset', 'balance': 0},
            '301': {'name': 'إيراد المبيعات', 'type': 'Revenue', 'balance': 0},
            '401': {'name': 'تكلفة البضاعة المباعة', 'type': 'Expense', 'balance': 0},
            '501': {'name': 'المصاريف العمومية', 'type': 'Expense', 'balance': 0}
        },
        # المستودع (الأصناف)
        'warehouse': {
            'صنف_1': {'qty': 100, 'cost': 50, 'price': 80},
            'صنف_2': {'qty': 50, 'cost': 120, 'price': 180}
        }
    }

# --- 3. محرك القيود المحاسبية (The Accounting Core) ---
def post_journal_entry(debit_entries, credit_entries, note):
    """وظيفة ترحيل القيود وضمان توازن النظام"""
    total_debit = sum([e['amount'] for e in debit_entries])
    total_credit = sum([e['amount'] for e in credit_entries])
    
    if total_debit != total_credit:
        return False, "خطأ: القيد غير متوازن!"

    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry_id = len(st.session_state.accounting_system['journal']) // 2 + 1
    
    for e in debit_entries + credit_entries:
        is_debit = e in debit_entries
        new_row = {
            'ID': entry_id, 'Date': date, 'Account_Code': e['code'],
            'Account_Name': st.session_state.accounting_system['chart_of_accounts'][e['code']]['name'],
            'Debit': e['amount'] if is_debit else 0,
            'Credit': 0 if is_debit else e['amount'],
            'Note': note
        }
        st.session_state.accounting_system['journal'] = pd.concat(
            [st.session_state.accounting_system['journal'], pd.DataFrame([new_row])], ignore_index=True
        )
    return True, "تم الترحيل بنجاح"

# --- 4. واجهة المستخدم الرسومية ---
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .header-box { background: #1e3a8a; color: white; padding: 20px; text-align: center; border-radius: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# القائمة الجانبية (الموديلات)
menu = st.sidebar.selectbox("القائمة البرمجية", ["لوحة التحكم", "فاتورة مبيعات", "المستودعات", "دفتر اليومية", "ميزان المراجعة"])

# --- موديول: لوحة التحكم ---
if menu == "لوحة التحكم":
    st.markdown("<div class='header-box'><h1>الخوارزمي للمحاسبة والمستودعات</h1></div>", unsafe_allow_html=True)
    df = st.session_state.accounting_system['journal']
    cash = df[df['Account_Code'] == '101']['Debit'].sum() - df[df['Account_Code'] == '101']['Credit'].sum()
    sales = df[df['Account_Code'] == '301']['Credit'].sum()
    
    c1, c2 = st.columns(2)
    c1.metric("💰 رصيد الصندوق", f"{cash:,.2f}")
    c2.metric("📈 إجمالي المبيعات", f"{sales:,.2f}")

# --- موديول: فاتورة مبيعات (الربط الكامل) ---
elif menu == "فاتورة مبيعات":
    st.header("🛒 تحرير فاتورة مبيعات")
    with st.form("sale_inv"):
        item_name = st.selectbox("اختر الصنف", list(st.session_state.accounting_system['warehouse'].keys()))
        qty = st.number_input("الكمية", min_value=1)
        price = st.session_state.accounting_system['warehouse'][item_name]['price']
        cost = st.session_state.accounting_system['warehouse'][item_name]['cost']
        st.info(f"سعر الوحدة: {price} | الإجمالي: {qty*price}")
        
        if st.form_submit_button("حفظ وترحيل"):
            total_sale = qty * price
            total_cost = qty * cost
            
            # قيد المبيعات (من الصندوق إلى المبيعات)
            post_journal_entry(
                [{'code': '101', 'amount': total_sale}], # مدين
                [{'code': '301', 'amount': total_sale}], # دائن
                f"فاتورة مبيعات صنف: {item_name}"
            )
            # تحديث المخزن (إنقاص الكمية)
            st.session_state.accounting_system['warehouse'][item_name]['qty'] -= qty
            st.success("تم الحفظ وتوليد القيود وتحديث المخازن!")

# --- موديول: ميزان المراجعة ---
elif menu == "ميزان المراجعة":
    st.header("⚖️ ميزان المراجعة بالأرصدة")
    df = st.session_state.accounting_system['journal']
    if not df.empty:
        trial_balance = df.groupby(['Account_Code', 'Account_Name']).agg({'Debit':'sum', 'Credit':'sum'})
        st.table(trial_balance)
    else:
        st.warning("لا توجد بيانات محاسبية بعد.")
