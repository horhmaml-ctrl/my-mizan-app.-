import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="الميزان المحمول", layout="centered")

# --- إدارة التنقل ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- CSS احترافي يضمن التناسق 100% ---
st.markdown("""
    <style>
    .block-container { padding: 0px !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #ffffff; }

    /* هيدر أزرق */
    .header {
        background-color: #2563eb; color: white; padding: 15px;
        text-align: center; font-weight: bold; font-size: 18px;
    }

    /* شبكة الأزرار العلوية */
    .top-actions {
        display: flex; justify-content: space-around;
        background: #f1f5f9; padding: 10px 5px; gap: 5px;
    }
    .top-btn {
        background: #3b82f6; color: white; border-radius: 5px;
        padding: 8px; font-size: 10px; flex: 1; text-align: center;
    }

    /* البطاقات الرئيسية - شبكة ثابتة لا تنكسر */
    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr; /* عمودين دائماً */
        gap: 15px;
        padding: 15px;
        margin-bottom: 80px;
    }

    /* زر مخفي فوق تصميم البطاقة */
    div.stButton > button {
        width: 100% !important;
        height: 100px !important;
        border-radius: 12px !important;
        background: white !important;
        border: 1.5px solid #dbeafe !important;
        color: #1e293b !important;
        font-weight: bold !important;
        font-size: 14px !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1) !important;
    }

    /* فوتر سفلي */
    .footer {
        position: fixed; bottom: 0; width: 100%;
        background: #1d4ed8; color: white;
        display: grid; grid-template-columns: 1fr 1fr 1fr;
        text-align: center; padding: 10px 0; font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- محتوى الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown("<div class='header'>نظام محاسبي متكامل</div>", unsafe_allow_html=True)
    
    # أزرار علوية سريعة
    c1, c2, c3 = st.columns(3)
    with c1: st.button("📄 سند جديد")
    with c2: 
        if st.button("➕ فاتورة"):
            st.session_state.page = 'invoice'
            st.rerun()
    with c3: st.button("🔍 بحث")

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # البطاقات الرئيسية (2x2)
    # نستخدم الأعمدة ولكن نضمن أنها لن تنكسر
    col_a, col_b = st.columns(2)
    with col_a:
        st.button("👤\nالعملاء", key="c1")
        st.button("🏢\nالموظفين", key="c3")
        st.button("🛒\nالمشتريات", key="c5")
    with col_b:
        st.button("🚚\nالموردين", key="c2")
        st.button("✂️\nالمصاريف", key="c4")
        st.button("📈\nالمبيعات", key="c6")

    st.markdown("""
        <div class='footer'>
            <div>الإيرادات<br>0.00</div>
            <div>المصروفات<br>0.00</div>
            <div>الأرباح<br>0.00</div>
        </div>
        """, unsafe_allow_html=True)

# --- صفحة الفاتورة ---
elif st.session_state.page == 'invoice':
    st.markdown("<div class='header'>فاتورة بيع</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"):
        st.session_state.page = 'home'
        st.rerun()
    st.text_input("اسم العميل")
    st.number_input("المبلغ")
    st.button("حفظ")
