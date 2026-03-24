import streamlit as st

# إعداد الصفحة لتكون تطبيق جوال
st.set_page_config(page_title="نظام المحاسبة", layout="centered")

# --- إدارة التنقل ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- كود التنسيق القسري (Forced Grid) ---
st.markdown("""
    <style>
    /* إلغاء جميع المسافات الافتراضية للمتصفح */
    .block-container { padding: 0px !important; max-width: 100% !important; }
    footer, header, #MainMenu {visibility: hidden;}
    
    /* خلفية التطبيق */
    .stApp { background-color: #f1f5f9; }

    /* الشريط العلوي */
    .top-header {
        background-color: #2563eb; color: white; padding: 15px;
        text-align: center; font-weight: bold; font-size: 18px;
        border-radius: 0 0 15px 15px; margin-bottom: 10px;
    }

    /* شبكة البطاقات 2x2 التي لا تنكسر */
    .mobile-grid {
        display: flex;
        flex-wrap: wrap;
        padding: 10px;
        justify-content: space-between;
    }

    /* تصميم الزر ليصبح مربعاً بجانب زميله */
    div.stButton > button {
        width: 48vw !important; /* يأخذ نصف عرض الشاشة تقريباً */
        height: 120px !important;
        margin-bottom: 10px !important;
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        display: flex !important;
        flex-direction: column !important;
        color: #1e293b !important;
        font-weight: bold !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }

    /* شريط المعلومات السفلي الثابت */
    .footer-fixed {
        position: fixed; bottom: 0; width: 100%;
        background-color: #1e40af; color: white;
        display: grid; grid-template-columns: repeat(3, 1fr);
        text-align: center; padding: 10px 0; font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- محتوى الصفحات ---

if st.session_state.page == 'home':
    st.markdown("<div class='top-header'>نظام محاسبي متكامل</div>", unsafe_allow_html=True)
    
    # شبكة الأزرار العلوية الصغيرة
    c_top1, c_top2, c_top3 = st.columns(3)
    with c_top1: st.button("📄 سندات")
    with c_top2: 
        if st.button("➕ فاتورة"):
            st.session_state.page = 'invoice'
            st.rerun()
    with c_top3: st.button("🔍 بحث")

    st.write("---")

    # هنا السر: الأزرار ستظهر 2 بجانب بعضها بسبب الـ CSS أعلاه (width: 48vw)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👤\nالعملاء\n0", key="c1"):
            st.session_state.page = 'customers'
            st.rerun()
        st.button("🏢\nالموظفين\n0", key="c3")
        st.button("📉\nالمشتريات\n0", key="c5")

    with col2:
        st.button("🚚\nالموردين\n0", key="c2")
        st.button("✂️\nالمصاريف\n0", key="c4")
        st.button("📈\nالمبيعات\n0", key="c6")

    # الفوتر الثابت
    st.markdown("""
        <div class='footer-fixed'>
            <div>الإيرادات<br>0.00</div>
            <div>المصروفات<br>0.00</div>
            <div>الأرباح<br>0.00</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == 'invoice':
    st.markdown("<div class='top-header'>فاتورة بيع جديدة</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"):
        st.session_state.page = 'home'
        st.rerun()
    st.text_input("اسم العميل")
    st.number_input("المبلغ")
    st.button("حفظ ✅")

elif st.session_state.page == 'customers':
    st.markdown("<div class='top-header'>دليل العملاء</div>", unsafe_allow_html=True)
    if st.button("🔙 عودة"):
        st.session_state.page = 'home'
        st.rerun()
    st.write("قائمة العملاء تظهر هنا...")
