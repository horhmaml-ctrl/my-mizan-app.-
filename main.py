import streamlit as st
import pandas as pd

# إعداد الصفحة وتغيير السمة للون البرتقالي والرمادي
st.set_page_config(page_title="نظام الميزان - واجهة الاختصارات", layout="wide")

# تصميم CSS متقدم للأزرار الكبيرة والاختصارات
st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .stButton>button {
        height: 100px;
        background-color: white;
        color: #FF8C00;
        border: 2px solid #FF8C00;
        border-radius: 15px;
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #FF8C00;
        color: white;
        transform: translateY(-5px);
    }
    .header-bar {
        background-color: #FF8C00;
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# تهيئة البيانات
if 'journal' not in st.session_state:
    st.session_state.journal = []
if 'view' not in st.session_state:
    st.session_state.view = "الرئيسية"

# ترويسة البرنامج
st.markdown("<div class='header-bar'><h1>🟠 نظام الميزان للمحاسبة والمستودعات - واجهة الاختصارات</h1></div>", unsafe_allow_html=True)

# --- شريط جانبي ثابت للعودة للرئيسية ---
if st.sidebar.button("🏠 العودة لسطح المكتب"):
    st.session_state.view = "الرئيسية"

st.sidebar.markdown("---")
st.sidebar.write("👤 المستخدم: المدير العام")
st.sidebar.write("📅 التاريخ: " + pd.Timestamp.now().strftime("%Y-%m-%d"))

# --- منطق العرض (التبديل بين الواجهات) ---

if st.session_state.view == "الرئيسية":
    st.subheader("⚡ الوصول السريع (الاختصارات)")
    
    # شبكة الاختصارات (4 أعمدة)
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
    
    with row1_col1:
        if st.button("🛒\nفاتورة بيع"):
            st.session_state.view = "فاتورة بيع"
            st.rerun()
            
    with row1_col2:
        if st.button("📦\nفاتورة شراء"):
            st.session_state.view = "فاتورة شراء"
            st.rerun()
            
    with row1_col3:
        if st.button("📥\nسند قبض"):
            st.session_state.view = "سند قبض"
            st.rerun()
            
    with row1_col4:
        if st.button("📤\nسند صرف"):
            st.session_state.view = "سند صرف"
            st.rerun()

    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
    
    with row2_col1:
        if st.button("👥\nأرصدة العملاء"):
            st.session_state.view = "أرصدة العملاء"
            st.rerun()
            
    with row2_col2:
        if st.button("🏭\nالتصنيع"):
            st.session_state.view = "التصنيع"
            st.rerun()
            
    with row2_col3:
        if st.button("⚖️\nميزان المراجعة"):
            st.session_state.view = "ميزان المراجعة"
            st.rerun()
            
    with row2_col4:
        if st.button("⚙️\nالإعدادات"):
            st.info("الإعدادات قيد التطوير")

    st.markdown("---")
    st.subheader("📊 نظرة عامة على السيولة")
    # عرض رسم بياني سريع أو ملخص أرقام
    df = pd.DataFrame(st.session_state.journal)
    if not df.empty:
        st.line_chart(df.groupby("التاريخ")["مدين"].sum())
    else:
        st.write("لا توجد حركات مالية لعرضها في الرسم البياني حالياً.")

# --- واجهات العمليات (تظهر عند الضغط على الاختصار) ---

elif st.session_state.view == "فاتورة بيع":
    st.header("📝 فاتورة بيع نقدية/آجلة")
    with st.form("sale"):
        customer = st.selectbox("العميل", ["عميل نقدي", "شركة التقنية", "مؤسسة النجاح"])
        amount = st.number_input("إجمالي الفاتورة", min_value=0.0)
        if st.form_submit_button("اعتماد وحفظ 🟠"):
            st.session_state.journal.append({"التاريخ": pd.Timestamp.now().strftime("%Y-%m-%d"), "البيان": f"بيع لـ {customer}", "مدين": amount, "دائن": 0})
            st.success("تم الحفظ والترحيل")
            
elif st.session_state.view == "سند قبض":
    st.header("📥 سند قبض نقدي")
    with st.form("receipt"):
        from_acc = st.text_input("استلمنا من السيد/السادة")
        amount = st.number_input("المبلغ", min_value=0.0)
        if st.form_submit_button("ترحيل السند"):
            st.session_state.journal.append({"التاريخ": pd.Timestamp.now().strftime("%Y-%m-%d"), "البيان": f"قبض من {from_acc}", "مدين": amount, "دائن": 0})
            st.success("تم الترحيل للصندوق")

elif st.session_state.view == "أرصدة العملاء":
    st.header("👥 كشف أرصدة العملاء")
    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("لا توجد بيانات عملاء")
