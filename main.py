import streamlit as st
import pandas as pd

# إعداد الصفحة لتكون مضغوطة ومناسبة للجوال تماماً
st.set_page_config(page_title="فاتورة الميزان", layout="centered")

# هندسة الواجهة (CSS) لتطابق الصورة حرفياً
st.markdown("""
    <style>
    /* إخفاء القوائم العلوية والسفلية لتبدو كتطبيق */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main { background-color: #f8faff; }
    
    /* الترويسة الزرقاء العلوية */
    .top-blue-bar {
        background-color: #3b9df5;
        color: white;
        padding: 5px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        border-radius: 0 0 10px 10px;
    }

    /* عنوان الفاتورة الوردي */
    .inv-title {
        color: #d81b60;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin: 5px 0;
    }

    /* تسميات الحقول الوردية */
    .pink-text { color: #d81b60; font-weight: bold; font-size: 14px; text-align: right; margin-bottom: 2px; }

    /* تنسيق الحقول لتكون صغيرة (Compact) */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        height: 35px !important;
        border-radius: 5px !important;
        border: 1px solid #3b9df5 !important;
    }

    /* شريط خيارات (بيع/شراء - نقدا/اجل) */
    .radio-group {
        display: flex;
        justify-content: space-between;
        background: white;
        padding: 5px;
        border: 1px solid #3b9df5;
        border-radius: 20px;
        margin: 5px 0;
    }

    /* الجدول الأزرق */
    .blue-table-header {
        background-color: #3b9df5;
        color: white;
        padding: 8px;
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        font-weight: bold;
        border-radius: 5px 5px 0 0;
    }
    
    /* صندوق الإجماليات السفلي */
    .totals-box {
        border: 1px solid #3b9df5;
        background: white;
        padding: 10px;
        border-radius: 10px;
        margin-top: 10px;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. الشريط العلوي (الساعة والباركود وحجم الورق)
st.markdown("""
    <div class='top-blue-bar'>
        <span>9:08 24/03/2026</span>
        <span>مقاس الورق: A4 🔘 | 80m ⚪</span>
        <span style='font-size: 20px;'>💾</span>
    </div>
    """, unsafe_allow_html=True)

# 2. العنوان ورقم الفاتورة
st.markdown("<div class='inv-title'>فاتورة بيع نقداً</div>", unsafe_allow_html=True)

c_inv_no, c_acc_label = st.columns([1, 2])
with c_inv_no:
    st.text_input("رقم الفاتورة", "3087", label_visibility="collapsed")
with c_acc_label:
    st.markdown("<div class='pink-text'>حساب الصندوق</div>", unsafe_allow_html=True)
    st.selectbox("حساب الصندوق", ["الصندوق الرئيسي", "صندوق العملات"], label_visibility="collapsed")

# 3. شريط الخيارات (نفس راديو الصورة)
col_opt1, col_opt2, col_opt3 = st.columns(3)
with col_opt1:
    st.radio("النوع", ["بيع", "شراء"], horizontal=True, label_visibility="collapsed")
with col_opt2:
    st.radio("الدفع", ["نقداً", "آجل"], horizontal=True, label_visibility="collapsed")
with col_opt3:
    st.checkbox("مرتجع")

# 4. البحث والملاحظات والمستودع
col_search, col_plus = st.columns([5, 1])
with col_search:
    st.text_input("البحث", placeholder="بحث عن حساب", label_visibility="collapsed")
with col_plus:
    st.button("➕")

st.text_input("الملاحظات", placeholder="ملاحظات", label_visibility="collapsed")

col_store, col_mic = st.columns([5, 1])
with col_store:
    st.selectbox("المخزن", ["مخزن بضاعة جاهزة", "المخزن الرئيسي"], label_visibility="collapsed")
with col_mic:
    st.markdown("<div style='text-align:center; font-size:20px; padding-top:5px;'>🎙️</div>", unsafe_allow_html=True)

# 5. منطقة الأصناف (إدخال الصنف)
col_item_search, col_barcode = st.columns([5, 1])
with col_item_search:
    st.text_input("صنف", placeholder="بحث عن صنف", label_visibility="collapsed")
with col_barcode:
    st.markdown("<div style='text-align:center; font-size:20px;'>📊</div>", unsafe_allow_html=True)

c_qty, c_price, c_add = st.columns([1, 1, 2])
with c_qty: st.text_input("العدد", "1")
with c_price: st.text_input("السعر", "0.00")
with c_add: st.button("إضافة صنف جديد")

# 6. الجدول (رأس الجدول الأزرق)
st.markdown("""
    <div class='blue-table-header'>
        <span>اسم الصنف</span>
        <span>الوحدة</span>
        <span>العدد</span>
        <span>السعر</span>
        <span>الاجمالي</span>
    </div>
    <div style='background: white; height: 100px; border: 1px solid #3b9df5; border-top: none;'></div>
    """, unsafe_allow_html=True)

# 7. الإجماليات والضرائب (التذييل)
st.markdown("<div class='totals-box'>", unsafe_allow_html=True)
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.write("عدد القطع: 0.00")
    st.text_input("الاجمالي", "0.00")
    st.text_input("صافي الفاتورة", "0.00")
with col_f2:
    st.number_input("نسبة الخصم %", 0)
    st.text_input("المبلغ المستلم", "0.00")
    st.number_input("نسبة الضريبة %", 0)
st.markdown("</div>", unsafe_allow_html=True)

# أزرار التنقل السفلية
st.markdown("---")
st.columns(3)[1].button("🏠")
