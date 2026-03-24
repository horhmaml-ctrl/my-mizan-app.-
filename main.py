import streamlit as st

# إعداد الصفحة لتكون نظيفة جداً
st.set_page_config(page_title="الميزان دوت نت", layout="centered")

# --- إدارة التنقل ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- تصميم CSS مستوحى من "الميزان" (الأزرق والوردي) ---
st.markdown("""
    <style>
    .block-container { padding: 10px !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0faff; }

    /* عنوان الفاتورة الوردي المميز */
    .inv-header {
        color: #e91e63; font-weight: bold; font-size: 24px;
        text-align: center; margin-bottom: 20px;
    }

    /* تصميم الحقول لتبدو كجداول الميزان */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border: 1px solid #3498db !important;
        border-radius: 5px !important;
    }

    /* الأزرار الزرقاء */
    div.stButton > button {
        background-color: #3498db !important;
        color: white !important;
        border-radius: 20px !important;
        width: 100% !important;
    }

    /* شريط المعلومات السفلي */
    .mizan-footer {
        background-color: white; border: 2px solid #3498db;
        border-radius: 10px; padding: 15px; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- واجهة الفاتورة (روح الميزان) ---
st.markdown("<div class='inv-header'>فاتورة بيع نقداً</div>", unsafe_allow_html=True)

# القسم الأول: البيانات الأساسية
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.text_input("رقم الفاتورة", value="3087")
    with col2:
        st.selectbox("حساب الصندوق", ["الصندوق الرئيسي", "صندوق المبيعات"])

# القسم الثاني: البحث والمخزن
st.text_input("🔍 بحث عن حساب (عميل)")
st.selectbox("المخزن", ["مخزن بضاعة جاهزة", "المخزن الرئيسي"])

st.markdown("---")

# القسم الثالث: إضافة المواد (الجدول التفاعلي)
col_m, col_q, col_p = st.columns([2, 1, 1])
with col_m:
    st.text_input("المادة", placeholder="اسم الصنف")
with col_q:
    st.text_input("العدد", value="1")
with col_p:
    st.text_input("السعر", value="0.00")

if st.button("➕ إضافة المادة للفاتورة"):
    st.success("تمت الإضافة للجدول")

# القسم الرابع: ملخص الفاتورة (الفوتر الأبيض)
st.markdown("<div class='mizan-footer'>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
with f1:
    st.write("**الإجمالي:** 0.00")
    st.write("**الضريبة (15%):** 0.00")
with f2:
    st.write("**الخصم:** 0.00")
    st.write("### **الصافي: 0.00**")
st.markdown("</div>", unsafe_allow_html=True)

# أزرار الحفظ والطباعة
st.write(" ")
save_col, print_col = st.columns(2)
with save_col:
    st.button("💾 حفظ الفاتورة")
with print_col:
    st.button("🖨️ طباعة")
