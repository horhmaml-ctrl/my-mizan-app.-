import streamlit as st
import pandas as pd

# إعدادات الواجهة والجوال
st.set_page_config(page_title="الميزان دوت نت - إدارة العمليات", layout="centered")

# تصميم الأزرار والواجهات (اللون البرتقالي الكلاسيكي)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 50px; background-color: white; color: #e67e22; border: 2px solid #e67e22; font-weight: bold; margin-bottom: 10px; }
    .header-style { background-color: #e67e22; color: white; padding: 10px; text-align: center; border-radius: 10px; margin-bottom: 20px; }
    .sub-card { background-color: #ffffff; padding: 15px; border-radius: 10px; border-right: 5px solid #e67e22; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- مخازن البيانات (قاعدة بيانات مصغرة داخل التطبيق) ---
if 'db' not in st.session_state:
    st.session_state.db = {
        'items': ['دقيق سندي', 'زيت طبخ', 'سكر مطحون'], # المواد والاصناف
        'accounts': {'1101': 'صندوق الرئيسي', '1201': 'شركة الأمل (مورد)', '1301': 'خالد محمد (عميل)'}, # شجرة الحسابات
        'invoices': [], # سجل الفواتير
        'current_view': 'الرئيسية' # واجهة التحكم
    }

# --- وظائف الملاحة (الرجوع للرئيسية) ---
def go_home(): st.session_state.db['current_view'] = 'الرئيسية'

# --- 1. واجهة سطح المكتب (الرئيسية) ---
if st.session_state.db['current_view'] == 'الرئيسية':
    st.markdown("<div class='header-style'><h2>📊 لوحة تحكم الميزان</h2></div>", unsafe_allow_html=True)
    
    # شبكة الأزرار (الاختصارات)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 فاتورة بيع"): st.session_state.db['current_view'] = 'فاتورة'
        if st.button("🌳 شجرة الحسابات"): st.session_state.db['current_view'] = 'شجرة'
        if st.button("🔍 بحث المواد"): st.session_state.db['current_view'] = 'بحث_مواد'
    with col2:
        if st.button("📑 كشف حساب"): st.session_state.db['current_view'] = 'كشف_حساب'
        if st.button("👤 إضافة/حذف حساب"): st.session_state.db['current_view'] = 'إدارة_حسابات'
        if st.button("💰 أرصدة العملاء"): st.session_state.db['current_view'] = 'أرصدة'
    
    st.divider()
    st.info("💡 تلميح: استخدم قائمة البحث للوصول السريع للمواد.")

# --- 2. واجهة الفواتير (بيع/شراء) ---
elif st.session_state.db['current_view'] == 'فاتورة':
    st.subheader("📝 إنشاء فاتورة جديدة")
    with st.form("inv_form"):
        target = st.selectbox("الحساب (العميل/المورد)", list(st.session_state.db['accounts'].values()))
        item = st.selectbox("المادة/الصنف", st.session_state.db['items'])
        qty = st.number_input("الكمية", min_value=1)
        price = st.number_input("السعر الإفرادي", min_value=0.0)
        total = qty * price
        st.write(f"### الإجمالي: {total} ريال")
        if st.form_submit_button("حفظ وترحيل الفاتورة 🟠"):
            st.session_state.db['invoices'].append({'التاريخ': '2026-03-24', 'الحساب': target, 'المادة': item, 'المبلغ': total})
            st.success("تم الترحيل بنجاح!")
    if st.button("🔙 عودة"): go_home()

# --- 3. واجهة شجرة الحسابات والبحث ---
elif st.session_state.db['current_view'] == 'شجرة':
    st.subheader("🌳 الشجرة المحاسبية")
    search_q = st.text_input("🔍 ابحث عن حساب (عميل، مورد، موظف)...")
    for code, name in st.session_state.db['accounts'].items():
        if search_q.lower() in name.lower() or search_q in code:
            st.markdown(f"<div class='sub-card'><b>{code}</b> - {name}</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"): go_home()

# --- 4. واجهة إضافة/حذف حساب ---
elif st.session_state.db['current_view'] == 'إدارة_حسابات':
    st.subheader("👤 إدارة الحسابات")
    tab1, tab2 = st.tabs(["➕ إضافة حساب", "🗑️ حذف حساب"])
    with tab1:
        new_code = st.text_input("رمز الحساب الجديد")
        new_name = st.text_input("اسم الحساب (العميل/المورد)")
        if st.button("إضافة للحسابات ✅"):
            st.session_state.db['accounts'][new_code] = new_name
            st.success(f"تمت إضافة {new_name}")
    with tab2:
        del_code = st.selectbox("اختر الحساب للحذف", list(st.session_state.db['accounts'].keys()))
        if st.button("تأكيد الحذف ❌"):
            del st.session_state.db['accounts'][del_code]
            st.warning("تم حذف الحساب")
    if st.button("🔙 عودة"): go_home()

# --- 5. بحث المواد والأصناف ---
elif st.session_state.db['current_view'] == 'بحث_مواد':
    st.subheader("📦 إدارة الأصناف والمواد")
    search_item = st.text_input("ابحث عن مادة...")
    for i in st.session_state.db['items']:
        if search_item.lower() in i.lower():
            st.write(f"📦 {i}")
    new_i = st.text_input("إضافة مادة جديدة للمستودع")
    if st.button("إضافة مادة"):
        st.session_state.db['items'].append(new_i)
        st.rerun()
    if st.button("🔙 عودة"): go_home()

# --- 6. كشف الحساب ---
elif st.session_state.db['current_view'] == 'كشف_حساب':
    st.subheader("📑 تقرير كشف حساب تفصيلي")
    acc_filter = st.selectbox("اختر الحساب", list(st.session_state.db['accounts'].values()))
    if st.session_state.db['invoices']:
        df = pd.DataFrame(st.session_state.db['invoices'])
        result = df[df['الحساب'] == acc_filter]
        st.table(result)
    else: st.warning("لا توجد حركات مسجلة لهذا الحساب")
    if st.button("🔙 عودة"): go_home()
