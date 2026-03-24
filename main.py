import streamlit as st
import pandas as pd

st.set_page_config(page_title="فاتورة بيع - الميزان", layout="centered")

# تصميم CSS لمحاكاة الألوان والأشكال في الصورة
st.markdown("""
    <style>
    .main { background-color: #f0faff; }
    .header-blue { background-color: #3498db; color: white; padding: 10px; border-radius: 0 0 20px 20px; text-align: center; }
    .invoice-title { color: #e91e63; text-align: center; font-weight: bold; font-size: 24px; margin-top: 10px; }
    .pink-label { color: #e91e63; font-weight: bold; text-align: right; }
    .stButton>button { border-radius: 20px; }
    .footer-table { background-color: white; border: 1px solid #3498db; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ترويسة الفاتورة (Header) ---
st.markdown("""
    <div class='header-blue'>
        <p style='float: left;'>9:08 24/03/2026</p>
        <p style='float: right;'>💾</p>
        <div style='clear: both;'></div>
        <p>مقاس الورق: 🔘 A4  ⚪ 80m</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='invoice-title'>فاتورة بيع نقداً</div>", unsafe_allow_html=True)

# --- مدخلات الفاتورة الأساسية ---
col_inv_no, col_acc = st.columns([1, 2])
with col_inv_no:
    st.text_input("رقم الفاتورة", value="3087")
with col_acc:
    st.markdown("<p class='pink-label'>حساب الصندوق</p>", unsafe_allow_html=True)
    st.selectbox("", ["الصندوق الرئيسي", "صندوق العملات"])

# خيارات البيع/الشراء/نقداً/آجل
c1, c2, c3, c4 = st.columns(4)
c1.radio("", ["بيع", "شراء"], horizontal=True, index=0)
c2.radio("", ["نقداً", "آجل"], horizontal=True, index=0)
c3.checkbox("مرتجع")

# البحث عن حساب وملاحظات
col_search, col_add = st.columns([4, 1])
with col_search:
    st.text_input("🔍 بحث عن حساب", placeholder="اكتب اسم العميل هنا...")
with col_add:
    st.markdown("## ➕")

st.text_area("ملاحظات", placeholder="أدخل الملاحظات هنا...", height=60)

# --- تفاصيل المادة (المستودع والصنف) ---
st.selectbox("مخزن بضاعة جاهزة", ["المخزن الرئيسي", "مخزن المعرض"])

col_item, col_qty, col_price = st.columns([2, 1, 1])
with col_item:
    st.text_input("البحث عن صنف", placeholder="اسم الصنف أو الباركود")
with col_qty:
    st.number_input("العدد", min_value=1)
with col_price:
    st.number_input("السعر")

st.button("اضافة صنف جديد")

# --- جدول الأصناف (الجدول الأزرق) ---
st.markdown("""
    <div style='background-color: #3498db; color: white; padding: 5px; text-align: center; display: flex; justify-content: space-around; border-radius: 5px;'>
        <span>اسم الصنف</span><span>الوحدة</span><span>العدد</span><span>السعر</span><span>الاجمالي</span>
    </div>
    """, unsafe_allow_html=True)
st.write("---") # مساحة للأصناف المضافة

# --- ملخص الفاتورة (التذييل السفلي) ---
st.markdown("<div class='footer-table'>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
with f1:
    st.text_input("الإجمالي", value="0.00", disabled=True)
    st.text_input("الخصم", value="0.00")
    st.text_input("الضريبة", value="0.00")
    st.text_input("صافي الفاتورة", value="0.00", disabled=True)
with f2:
    st.write("عدد القطع: 0.00")
    st.number_input("نسبة الخصم %", value=0)
    st.number_input("المبلغ المستلم", value=0.0)
    st.number_input("نسبة الضريبة %", value=0)
st.markdown("</div>", unsafe_allow_html=True)

# أزرار التنقل السفلية
st.markdown("---")
st.columns(5)[2].button("🏠")
