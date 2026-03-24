import streamlit as st

# 1. إعدادات أساسية للجوال
st.set_page_config(page_title="الميزان برو", layout="centered")

# 2. نظام التنقل
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# 3. تصميم CSS "شامل وقوي" لإصلاح كل العيوب السابقة
st.markdown("""
    <style>
    .block-container { padding: 0px !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f1f5f9; }

    /* الهيدر */
    .app-header {
        background-color: #2563eb; color: white; padding: 15px;
        text-align: center; font-weight: bold; font-size: 18px;
    }

    /* إصلاح تباعد الأعمدة على الجوال */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 calc(33.33% - 10px) !important;
        min-width: calc(33.33% - 10px) !important;
    }
    
    /* تصميم الأزرار العلوية (3 أعمدة) */
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        border-radius: 8px !important;
        font-size: 11px !important;
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
        margin-bottom: 5px !important;
    }

    /* تصميم البطاقات السفلية (2 عمود) */
    .card-zone div.stButton > button {
        height: 120px !important;
        background-color: white !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        font-size: 14px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }

    /* الفوتر */
    .footer {
        position: fixed; bottom: 0; width: 100%;
        background-color: #1e40af; color: white;
        display: grid; grid-template-columns: repeat(3, 1fr);
        text-align: center; padding: 10px 0; font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- محتوى الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown("<div class='app-header'>نظام محاسبي متكامل</div>", unsafe_allow_html=True)

    # النصف العلوي: 3 أعمدة متساوية
    st.write(" ") # مسافة بسيطة
    t1, t2, t3 = st.columns(3)
    with t1:
        st.button("📄 سند صرف")
        st.button("🔍 كشف حساب")
    with t2:
        if st.button("➕ فاتورة"):
            st.session_state.page = 'invoice'
            st.rerun()
        st.button("💱 صرف عملة")
    with t3:
        st.button("📝 قيد عام")
        st.button("📊 مراجعة")

    st.markdown("<hr style='margin:10px;'>", unsafe_allow_html=True)

    # النصف السفلي: البطاقات (2 عمود)
    st.markdown("<div class='card-zone'>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        st.button("👤\nالعملاء\n0", key="k1")
        st.button("🏢\nالموظفين\n0", key="k3")
        st.button("🛒\nالمشتريات\n0", key="k5")
    with b2:
        st.button("🚚\nالموردين\n0", key="k2")
        st.button("📉\nالمبيعات\n0", key="k4")
        st.button("✂️\nالمصاريف\n0", key="k6")
    st.markdown("</div>", unsafe_allow_html=True)

    # الفوتر الثابت
    st.markdown("""
        <div class='footer'>
            <div>الإيرادات<br>0.00</div>
            <div>المصروفات<br>0.00</div>
            <div>الأرباح<br>0.00</div>
        </div>
        """, unsafe_allow_html=True)

# --- صفحة الفاتورة ---
elif st.session_state.page == 'invoice':
    st.markdown("<div class='app-header'>إضافة فاتورة</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.text_input("اسم العميل")
    st.number_input("المبلغ الإجمالي")
    st.button("حفظ الفاتورة ✅")
