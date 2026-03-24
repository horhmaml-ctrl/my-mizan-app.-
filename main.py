import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="النظام المحاسبي المتكامل", layout="centered")

# --- إدارة الحالة (Navigation) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- التصميم المتقدم (CSS) لجعل الأزرار غير مرئية وفوق الصور ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #f8fafc; }
    
    /* تنسيق الحاوية الرئيسية */
    .main-container { padding: 10px; margin-bottom: 70px; }
    
    /* تصميم البطاقة التفاعلية */
    div.stButton > button {
        background-color: white;
        border: 1px solid #bfdbfe;
        border-radius: 15px;
        height: 120px !important;
        width: 100%;
        color: #1e293b;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        transition: 0.2s;
    }
    div.stButton > button:hover {
        border-color: #3b82f6;
        background-color: #eff6ff;
        transform: scale(1.02);
    }
    
    /* الشريط العلوي */
    .app-header {
        background-color: #2563eb; color: white; padding: 15px;
        text-align: center; font-weight: bold; border-radius: 0 0 15px 15px;
        margin-bottom: 10px;
    }

    /* الفوتر السفلي */
    .footer-bar {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: #1d4ed8; color: white;
        display: grid; grid-template-columns: repeat(3, 1fr);
        text-align: center; padding: 10px 0; font-size: 11px; z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- منطق التنقل بين الصفحات ---

# 1. الصفحة الرئيسية (واجهة البطاقات)
if st.session_state.page == 'home':
    st.markdown("<div class='app-header'>نظام محاسبي متكامل</div>", unsafe_allow_html=True)
    
    # شبكة الوصول السريع (الأزرار الصغيرة العلوية)
    c1, c2, c3 = st.columns(3)
    with c1: st.button("📄 سندات", on_click=lambda: st.info("فتح السندات"))
    with c2: st.button("➕ فاتورة", on_click=lambda: setattr(st.session_state, 'page', 'invoice'))
    with c3: st.button("🔍 كشف حساب")

    st.write("---")

    # شبكة البطاقات الرئيسية (2x2)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👤\nالعملاء\n0"):
            st.session_state.page = 'customers'
        if st.button("🏢\nالموظفين\n0"):
            st.info("صفحة الموظفين")
        if st.button("📉\nالمشتريات\n0"):
            st.info("صفحة المشتريات")
            
    with col2:
        if st.button("🚚\nالموردين\n0"):
            st.info("صفحة الموردين")
        if st.button("✂️\nالمصاريف\n0"):
            st.info("صفحة المصاريف")
        if st.button("📈\nالمبيعات\n0"):
            st.session_state.page = 'sales_report'

    st.markdown("""
        <div class='footer-bar'>
            <div>الإيرادات<br>0.00</div>
            <div>المصروفات<br>0.00</div>
            <div>الأرباح<br>0.00</div>
        </div>
        """, unsafe_allow_html=True)

# 2. صفحة فاتورة البيع (المطابقة للصورة السابقة)
elif st.session_state.page == 'invoice':
    st.markdown("<div class='app-header'>فاتورة بيع جديدة</div>", unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    
    # هنا نضع كود الفاتورة الذي صممناه سابقاً
    st.text_input("رقم الفاتورة", "3087")
    st.selectbox("حساب الصندوق", ["الصندوق الرئيسي", "صندوق العملات"])
    st.number_input("الكمية", min_value=1)
    st.button("حفظ الفاتورة ✅")

# 3. صفحة العملاء
elif st.session_state.page == 'customers':
    st.subheader("👥 دليل العملاء")
    if st.button("🔙 عودة"):
        st.session_state.page = 'home'
        st.rerun()
    st.write("قائمة العملاء المسجلين تظهر هنا...")
    st.text_input("إضافة عميل جديد")
