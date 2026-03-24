import streamlit as st

# إعداد الصفحة كأنها تطبيق أندرويد
st.set_page_config(page_title="نظام الميزان المتكامل", layout="centered", initial_sidebar_state="collapsed")

# --- إدارة التنقل (Navigation) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- هندسة الواجهة CSS (لضبط التناسق 100%) ---
st.markdown("""
    <style>
    /* إلغاء الفراغات العلوية والسفلية */
    .block-container { padding: 0px !important; margin: 0px !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f1f5f9; }

    /* الشريط العلوي الأزرق */
    .app-header {
        background-color: #2563eb; color: white; padding: 15px;
        text-align: center; font-weight: bold; font-size: 18px;
        border-radius: 0 0 15px 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    /* شبكة البطاقات (Grid) 2x2 */
    .cards-grid {
        display: grid;
        grid-template-columns: 1fr 1fr; /* عمودين متساويين دائماً */
        gap: 12px;
        padding: 15px;
        margin-bottom: 70px;
    }

    /* تصميم الزر ليبدو كبطاقة */
    .stButton > button {
        width: 100% !important;
        height: 130px !important;
        background-color: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 15px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.3s !important;
    }
    .stButton > button:hover {
        border-color: #3b82f6 !important;
        background-color: #f0f9ff !important;
    }

    /* شريط المعلومات السفلي الثابت */
    .status-footer {
        position: fixed; bottom: 0; width: 100%;
        background-color: #1e40af; color: white;
        display: grid; grid-template-columns: 1fr 1fr 1fr;
        text-align: center; padding: 10px 0; font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- محتوى الصفحات ---

# 1. الصفحة الرئيسية
if st.session_state.page == 'home':
    st.markdown("<div class='app-header'>نظام محاسبي متكامل</div>", unsafe_allow_html=True)
    
    # شبكة الأزرار العلوية الصغيرة (3 أعمدة)
    top_c1, top_c2, top_c3 = st.columns(3)
    with top_c1: st.button("📄 سندات")
    with top_c2: 
        if st.button("➕ فاتورة"):
            st.session_state.page = 'invoice'
            st.rerun()
    with top_c3: st.button("🔍 بحث")

    # شبكة البطاقات الرئيسية (2x2) - هنا نضمن التناسق
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👤\nالعملاء\n0", key="cust"):
            st.session_state.page = 'customers'
            st.rerun()
        if st.button("🏢\nالموظفين\n0", key="emp"): pass
        if st.button("📉\nالمشتريات\n0", key="purch"): pass

    with col2:
        if st.button("🚚\nالموردين\n0", key="supp"): pass
        if st.button("✂️\nالمصاريف\n0", key="exp"): pass
        if st.button("📈\nالمبيعات\n0", key="sales"): pass

    # الفوتر السفلي
    st.markdown("""
        <div class='status-footer'>
            <div>الإيرادات<br>0.00</div>
            <div>المصروفات<br>0.00</div>
            <div>الأرباح<br>0.00</div>
        </div>
        """, unsafe_allow_html=True)

# 2. صفحة الفاتورة (مثال للتنقل)
elif st.session_state.page == 'invoice':
    st.markdown("<div class='app-header'>فاتورة بيع نقداً</div>", unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.info("قم بإدخال بيانات الفاتورة هنا...")
    st.text_input("اسم العميل")
    st.number_input("المبلغ")
    st.button("حفظ ✅")

# 3. صفحة العملاء
elif st.session_state.page == 'customers':
    st.markdown("<div class='app-header'>دليل العملاء</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"):
        st.session_state.page = 'home'
        st.rerun()
    st.text_input("🔍 بحث عن عميل")
    st.write("لا يوجد عملاء حالياً")
