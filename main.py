import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات النظام
st.set_page_config(page_title="الخوارزمي دوت نت - المحرك المالي", layout="wide")

# 2. قاعدة البيانات المركزية (تخزين دائم للجلسة)
if 'data' not in st.session_state:
    st.session_state.data = {
        'journal': pd.DataFrame(columns=['رقم', 'التاريخ', 'الحساب', 'مدين', 'دائن', 'البيان']),
        'inventory': {'صنف ممتاز': {'qty': 100, 'price': 550}, 'صنف عادي': {'qty': 200, 'price': 120}},
        'cash_accounts': {'الصندوق الرئيسي': 380500.00, 'صرافة السنيري': 13068955.00},
        'page': 'dashboard'
    }

# --- وظيفة الترحيل الآلي (The Posting Logic) ---
def process_sale(item, qty, price, acc_name):
    total = qty * price
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    inv_no = len(st.session_state.data['journal']) // 2 + 1
    
    # 1. تحديث المخزن
    st.session_state.data['inventory'][item]['qty'] -= qty
    
    # 2. تحديث رصيد الحساب
    st.session_state.data['cash_accounts'][acc_name] += total
    
    # 3. توليد القيد المزدوج (مدين/دائن)
    new_entries = [
        {'رقم': inv_no, 'التاريخ': date, 'الحساب': acc_name, 'مدين': total, 'دائن': 0, 'البيان': f"مبيعات {item}"},
        {'رقم': inv_no, 'التاريخ': date, 'الحساب': 'إيراد المبيعات', 'مدين': 0, 'دائن': total, 'البيان': f"مبيعات {item}"}
    ]
    st.session_state.data['journal'] = pd.concat([st.session_state.data['journal'], pd.DataFrame(new_entries)], ignore_index=True)

# --- واجهة المستخدم (تصميم الميزان) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f6f9; }
    .mizan-header { background: #d35400; color: white; padding: 15px; font-weight: bold; border-radius: 0 0 10px 10px; }
    .stat-card { background: white; padding: 10px; border: 1px solid #ddd; border-radius: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# الهيدر
st.markdown("<div class='mizan-header'>الخوارزمي دوت نت - نظام إدارة المبيعات والمخازن</div>", unsafe_allow_html=True)

# التنقل بين الصفحات
if st.session_state.data['page'] == 'dashboard':
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.write("### 🔗 العمليات الرئيسية")
        if st.button("📄 فتح فاتورة مبيعات جديدة", use_container_width=True):
            st.session_state.data['page'] = 'invoice'
            st.rerun()
        
        st.write("---")
        st.write("### 🏦 أرصدة الصناديق الحالية")
        for acc, bal in st.session_state.data['cash_accounts'].items():
            st.info(f"**{acc}:** {bal:,.2f}")

    with col1:
        st.write("### 📦 حالة المخزن")
        for item, info in st.session_state.data['inventory'].items():
            st.warning(f"**{item}:** المتبقي ({info['qty']}) قطعة")

# --- شاشة الفاتورة (محاكاة الميزان) ---
elif st.session_state.data['page'] == 'invoice':
    st.subheader("📝 تحرير فاتورة مبيعات")
    
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            item_selected = st.selectbox("اختر الصنف", list(st.session_state.data['inventory'].keys()))
            acc_selected = st.selectbox("الحساب المتأثر (مدين)", list(st.session_state.data['cash_accounts'].keys()))
        with c2:
            qty_input = st.number_input("الكمية", min_value=1, value=1)
            unit_price = st.session_state.data['inventory'][item_selected]['price']
            st.write(f"**سعر الوحدة:** {unit_price}")
            st.write(f"## الإجمالي: {qty_input * unit_price:,.2f}")

    if st.button("✅ حفظ وترحيل الفاتورة", use_container_width=True):
        process_sale(item_selected, qty_input, unit_price, acc_selected)
        st.success("تم الحفظ! تم تحديث المخزن وترحيل القيد آلياً.")
        st.session_state.data['page'] = 'dashboard'
        st.rerun()

    if st.button("🔙 إلغاء والعودة"):
        st.session_state.data['page'] = 'dashboard'
        st.rerun()
