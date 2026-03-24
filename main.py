import streamlit as st

st.set_page_config(page_title="نظام الميزان الذكي", layout="centered")

# إدارة الصفحات (Navigation)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- تصميم CSS متطور للأزرار التفاعلية ---
st.markdown("""
    <style>
    .block-container { padding: 0px !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f8fafc; }

    /* الهيدر */
    .app-header {
        background-color: #2563eb; color: white; padding: 15px;
        text-align: center; font-weight: bold; font-size: 18px;
    }

    /* تنسيق الأزرار العلوية الصغيرة (3 أعمدة) */
    div.stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 12px !important;
    }
    
    /* تنسيق خاص لأزرار البطاقات السفلية (2 عمود) */
    .card-btn-container [data-testid="stVerticalBlock"] > div {
        background: white;
        border: 1px solid #cbd5e1;
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .footer-fixed {
        position: fixed; bottom: 0; width: 100%;
        background-color: #1e40af; color: white;
        display: grid; grid-template-columns: repeat(3, 1fr);
        text-align: center; padding: 10px 0; font-size: 11px; z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

# --- محتوى الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown("<div class='app-header'>نظام محاسبي متكامل</div>", unsafe_allow_html=True)

    # 1. النصف العلوي (3 أعمدة) - أزرار تفاعلية حقيقية
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1: 
            st.button("📄 سند صرف", key="b1")
            st.button("📊 مراجعة", key="b4")
        with c2: 
            if st.button("➕ فاتورة", key="b2"):
                st.session_state.page = 'invoice'
                st.rerun()
            st.button("💱 صرف", key="b5")
        with c3: 
            st.button("📝 قيد عام", key="b3")
            st.button("🔍 كشف حساب", key="b6")

    st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)

    # 2. النصف السفلي (2 عمود) - بطاقات تفاعلية
    col_left, col_right = st.columns(2)
    
    with col_right:
        if st.button("👤\nالعملاء\n0", key="c_cust"):
            st.session_state.page = 'customers'
            st.rerun()
        st.button("📈\nالمبيعات\n0", key="c_sales")
        st.button("🏢\nالموظفين\n0", key="c_emp")

    with col_left:
        st.button("🚚\nالموردين\n0", key="c_supp")
        st.button("📉\nالمشتريات\n0", key="c_purch")
        st.button("✂️\nالمصاريف\n0", key="c_exp")

    # الفوتر الثابت
    st.markdown("""
        <div class='footer-fixed'>
            <div>الإيرادات<br>0.00</div>
            <div>المصروفات<br>0.00</div>
            <div>الأرباح<br>0.00</div>
        </div>
        """, unsafe_allow_html=True)

# --- صفحة الفاتورة (مثال) ---
elif st.session_state.page == 'invoice':
    st.markdown("<div class='app-header'>فاتورة بيع جديدة</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    st.text_input("اسم العميل")
    st.number_input("المبلغ")
    st.button("حفظ ✅")

# --- صفحة العملاء ---
elif st.session_state.page == 'customers':
    st.markdown("<div class='app-header'>دليل العملاء</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"):
        st.session_state.page = 'home'
        st.rerun()
    st.write("قائمة العملاء تظهر هنا...")
