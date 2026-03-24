import streamlit as st
import pandas as pd

# إعداد الصفحة للجوال
st.set_page_config(page_title="الميزان - تخصيص الواجهة", layout="centered")

# تصميم CSS للأزرار والقوائم
st.markdown("""
    <style>
    .main { background-color: #f3f4f6; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 55px;
        background-color: white; color: #e67e22;
        border: 2px solid #e67e22; font-weight: bold;
    }
    .header-style {
        background-color: #e67e22; color: white;
        padding: 10px; text-align: center; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- إعدادات المستخدم في القائمة الجانبية (الاختيار والترتيب) ---
st.sidebar.header("⚙️ إعدادات واجهة المستخدم")
st.sidebar.subheader("1. اختر الأقسام الظاهرة")
show_accounts = st.sidebar.checkbox("أرصدة الحسابات", value=True)
show_quick_ops = st.sidebar.checkbox("العمليات السريعة", value=True)
show_alerts = st.sidebar.checkbox("التنبيهات", value=True)

st.sidebar.subheader("2. ترتيب العرض (من الأعلى للأسفل)")
order = st.sidebar.multiselect(
    "اسحب لإعادة الترتيب:",
    ["الحسابات", "العمليات السريعة", "التنبيهات"],
    default=["الحسابات", "العمليات السريعة", "التنبيهات"]
)

st.sidebar.subheader("3. تخصيص أزرار العمليات")
selected_ops = st.sidebar.multiselect(
    "إضافة/حذف أزرار الاختصارات:",
    ["فاتورة مبيع", "فاتورة شراء", "سند صرف", "سند قبض", "أرصدة العملاء", "طلب تصنيع"],
    default=["فاتورة مبيع", "سند صرف", "أرصدة العملاء"]
)

# --- تنفيذ الواجهة بناءً على اختياراتك ---
st.markdown("<div class='header-style'><h3>الميزان دوت نت - تخصيصي</h3></div>", unsafe_allow_html=True)

# دالة لعرض الحسابات
def display_accounts():
    with st.expander("💰 أرصدة الحسابات", expanded=True):
        data = {
            "الحساب": ["صندوق يمني", "صندوق سعودي", "صرافة السيري"],
            "الرصيد": ["380,500", "5,000", "13,068,955"]
        }
        st.table(pd.DataFrame(data))

# دالة لعرض العمليات السريعة
def display_quick_ops():
    st.subheader("⚡ العمليات المختارة")
    if not selected_ops:
        st.write("لا توجد أزرار مختارة. أضف من القائمة الجانبية.")
    else:
        # توزيع الأزرار في صفوف (2 في كل صف)
        cols = st.columns(2)
        for idx, op in enumerate(selected_ops):
            with cols[idx % 2]:
                if st.button(op):
                    st.success(f"فتح واجهة: {op}")

# دالة لعرض التنبيهات
def display_alerts():
    with st.expander("⚠️ التنبيهات النظامية"):
        st.error("آخر نسخة احتياطية: منذ 24 ساعة")
        st.warning("هناك 3 فواتير بيع لم ترحل بعد")

# عرض الأقسام حسب الترتيب المختار
for section in order:
    if section == "الحسابات" and show_accounts:
        display_accounts()
    elif section == "العمليات السريعة" and show_quick_ops:
        display_quick_ops()
    elif section == "التنبيهات" and show_alerts:
        display_alerts()

st.markdown("---")
st.caption("نسخة الجوال المرنة v2.0 - نظام الميزان")
