import streamlit as st
import pandas as pd

# إعداد الصفحة للجوال
st.set_page_config(page_title="الميزان Mobile", layout="centered")

# تصميم CSS مخصص للجوال (أزرار كبيرة، خطوط واضحة، ألوان الميزان)
st.markdown("""
    <style>
    .main { background-color: #f3f4f6; }
    /* ترويسة علوية نحيفة */
    .mobile-header {
        background-color: #e67e22;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 0 0 15px 15px;
        margin-bottom: 15px;
    }
    /* أزرار الاختصارات الملونة */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        background-color: white;
        color: #e67e22;
        border: 1px solid #e67e22;
        font-weight: bold;
        margin-bottom: 5px;
    }
    /* تنسيق الجداول للجوال */
    .stTable { font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 1. الترويسة العلوية (Header)
st.markdown("""
    <div class='mobile-header'>
        <h3 style='margin:0;'>الميزان دوت نت</h3>
        <p style='font-size:12px; margin:0;'>03:40 PM | June 25</p>
    </div>
    """, unsafe_allow_html=True)

# 2. قسم الحسابات (الأرصدة الحالية) - مفتوح افتراضياً
with st.expander("💰 أرصدة الحسابات والصناديق", expanded=True):
    data = {
        "الحساب": ["صندوق", "صندوق العملات", "صرافة السيري"],
        "الرصيد": ["380,500", "0.00", "13,068,955"]
    }
    st.table(pd.DataFrame(data))

# 3. قسم الاختصارات (أهم العمليات)
st.subheader("⚡ عمليات سريعة")
col1, col2 = st.columns(2)

with col1:
    if st.button("📄 فاتورة مبيع"):
        st.info("جاري فتح واجهة البيع...")
    if st.button("🛒 فاتورة شراء"):
        pass

with col2:
    if st.button("💸 سند صرف"):
        pass
    if st.button("📥 سند قبض"):
        pass

if st.button("👥 كشف أرصدة العملاء"):
    pass

# 4. التنبيهات وتلميح اليوم (قابلة للطي لتوفير المساحة)
with st.expander("⚠️ التنبيهات والتلميحات"):
    st.error("آخر نسخة احتياطية: 06/25/2023")
    st.info("تلميح: يمكنك استخدام البارcode لتسريع البيع.")

# 5. معلومات المستخدم (أسفل الصفحة)
st.markdown("---")
st.caption("👤 مسؤول النظام: ABO OMER2023")
st.caption("📍 الفرع الرئيسي | النسخة المحمولة v1.0")

# شريط سفلي ثابت (اختياري)
st.markdown("""
    <div style='text-align:center; padding:10px; color:#999; font-size:10px;'>
        جميع الحقوق محفوظة - نظام الميزان 2026
    </div>
    """, unsafe_allow_html=True)
