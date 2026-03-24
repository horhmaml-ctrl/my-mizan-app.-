import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات النظام المحاسبي
st.set_page_config(page_title="الخوارزمي دوت نت - التقارير المالية", layout="wide")

# 2. تهيئة البيانات (قاعدة بيانات الجلسة)
if 'data' not in st.session_state:
    st.session_state.data = {
        'journal': pd.DataFrame(columns=['رقم_القيد', 'التاريخ', 'الحساب', 'البيان', 'مدين', 'دائن']),
        'inventory': {'صنف ممتاز': {'qty': 100, 'price': 550}, 'صنف عادي': {'qty': 200, 'price': 120}},
        'cash_accounts': {'الصندوق الرئيسي': 380500.00, 'صرافة السنيري': 13068955.00},
        'page': 'dashboard'
    }

# --- وظيفة الترحيل المحاسبي (Posting Engine) ---
def process_sale(item, qty, price, acc_name):
    total = qty * price
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    inv_no = len(st.session_state.data['journal']) // 2 + 1
    
    # تحديث المخزن والأرصدة
    st.session_state.data['inventory'][item]['qty'] -= qty
    st.session_state.data['cash_accounts'][acc_name] += total
    
    # القيد المزدوج
    entry_debit = {'رقم_القيد': inv_no, 'التاريخ': date, 'الحساب': acc_name, 'البيان': f"مبيعات {item}", 'مدين': total, 'دائن': 0}
    entry_credit = {'رقم_القيد': inv_no, 'التاريخ': date, 'الحساب': 'إيراد المبيعات', 'البيان': f"مبيعات {item}", 'مدين': 0, 'دائن': total}
    
    st.session_state.data['journal'] = pd.concat([st.session_state.data['journal'], pd.DataFrame([entry_debit, entry_credit])], ignore_index=True)

# --- تنسيق الواجهة ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .header-mizan { background: #1e3a8a; color: white; padding: 15px; font-weight: bold; border-radius: 0 0 10px 10px; text-align: center; }
    .report-table { width: 100%; border-collapse: collapse; background: white; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='header-mizan'>نظام الخوارزمي - كشوفات الحسابات والمبيعات</div>", unsafe_allow_html=True)

# --- التنقل بين الموديلات ---
menu = st.sidebar.radio("قائمة النظام", ["لوحة التحكم", "فاتورة مبيعات", "كشف حساب تفصيلي"])

# 1. لوحة التحكم
if menu == "لوحة التحكم":
    st.write("### 📊 حالة الحسابات والمخازن")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**أرصدة الصناديق والسنيري**")
        st.dataframe(pd.DataFrame(st.session_state.data['cash_accounts'].items(), columns=['الحساب', 'الرصيد الحقيقي']))
    with c2:
        st.write("**حالة المستودع**")
        st.table(pd.DataFrame(st.session_state.data['inventory']).T)

# 2. فاتورة مبيعات
elif menu == "فاتورة مبيعات":
    st.subheader("🛒 إضافة فاتورة جديدة")
    with st.form("invoice"):
        col_a, col_b = st.columns(2)
        item = col_a.selectbox("الصنف", list(st.session_state.data['inventory'].keys()))
        acc = col_b.selectbox("الحساب المدين", list(st.session_state.data['cash_accounts'].keys()))
        qty = col_a.number_input("الكمية", min_value=1, value=1)
        price = st.session_state.data['inventory'][item]['price']
        st.info(f"إجمالي الفاتورة: {qty * price:,.2f}")
        
        if st.form_submit_button("حفظ وترحيل"):
            process_sale(item, qty, price, acc)
            st.success("تم ترحيل الفاتورة بنجاح!")

# 3. كشف حساب تفصيلي (محاكاة الميزان 100%)
elif menu == "كشف حساب تفصيلي":
    st.subheader("🔍 كشف حساب حركات الصناديق والعملاء")
    target_acc = st.selectbox("اختر الحساب لعرض حركاته", list(st.session_state.data['cash_accounts'].keys()) + ['إيراد المبيعات'])
    
    # تصفية البيانات للحساب المختار
    ledger_df = st.session_state.data['journal'][st.session_state.data['journal']['الحساب'] == target_acc].copy()
    
    if not ledger_df.empty:
        # حساب الرصيد التراكمي
        ledger_df['الرصيد'] = ledger_df['مدين'].cumsum() - ledger_df['دائن'].cumsum()
        
        # تنسيق العرض
        st.table(ledger_df[['التاريخ', 'البيان', 'مدين', 'دائن', 'الرصيد']])
        
        # الملخص النهائي
        final_bal = ledger_df['الرصيد'].iloc[-1]
        st.metric(f"الرصيد الختامي لـ {target_acc}", f"{final_bal:,.2f}")
    else:
        st.warning("لا توجد حركات مسجلة لهذا الحساب.")
