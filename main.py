import streamlit as st
import pandas as pd

# إعداد الصفحة لتطابق أبعاد البرامج المكتبية
st.set_page_config(page_title="الميزان دوت نت للمحاسبة", layout="wide")

# تصميم CSS مكثف لمحاكاة واجهة الصورة (البرتقالي، الرمادي، والجداول)
st.markdown("""
    <style>
    .main { background-color: #d1d5db; }
    .block-container { padding-top: 1rem; }
    /* ستايل البلوكات (الخانات) */
    .mizan-panel {
        background-color: #f3f4f6;
        border: 2px solid #e67e22;
        border-top: 25px solid #e67e22;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 15px;
        position: relative;
    }
    .panel-title {
        color: white;
        font-weight: bold;
        position: absolute;
        top: -24px;
        right: 10px;
        font-size: 14px;
    }
    .shortcut-item {
        color: #2c3e50;
        text-decoration: none;
        display: block;
        padding: 5px;
        border-bottom: 1px solid #ddd;
        text-align: right;
        font-size: 13px;
    }
    .shortcut-item:hover { background-color: #ffe0b2; }
    </style>
    """, unsafe_allow_html=True)

# ترويسة البرنامج العلوية
c_head1, c_head2 = st.columns([1, 4])
with c_head1:
    st.markdown("<h2 style='color: #e67e22;'>03:40</h2><p>June 25, Sunday</p>", unsafe_allow_html=True)
with c_head2:
    st.markdown("<div style='text-align: left;'><h1 style='color: #e67e22; margin:0;'>الميزان دوت نت</h1><p>للمحاسبة والمستودعات</p></div>", unsafe_allow_html=True)

# تقسيم الصفحة (3 أعمدة كما في الصورة)
col_left, col_mid, col_right = st.columns([1.5, 2, 1.5])

# --- العمود الأيمن (مسؤول النظام والاختصارات) ---
with col_right:
    st.markdown("""<div class='mizan-panel'><span class='panel-title'>مسؤول النظام</span>
    <p style='text-align:center;'><b>ABO OMER2023</b><br>(local)<br>الفترة 1<br>[2023/12/31 - 2022/12/26]</p>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<div class='mizan-panel'><span class='panel-title'>📑 الاختصارات</span>", unsafe_allow_html=True)
    if st.button("📄 فاتورة مبيع آجل"): pass
    if st.button("💸 سند صرف"): pass
    if st.button("🛒 فاتورة شراء آجل"): pass
    if st.button("📦 إدخال بضاعة جاهزة"): pass
    if st.button("👥 أرصدة العملاء"): pass
    st.markdown("</div>", unsafe_allow_html=True)

# --- العمود الأوسط (الحسابات) ---
with col_mid:
    st.markdown("<div class='mizan-panel'><span class='panel-title'>💰 الحسابات</span>", unsafe_allow_html=True)
    # جدول الحسابات كما في الصورة
    data = {
        "الحساب": ["صندوق", "صندوق العملات", "صرافة السيري يمني", "صرافة السيري عملات"],
        "العملة": ["ريال يمني", "ريال سعودي", "ريال يمني", "ريال سعودي"],
        "الرصيد": ["380,500.00", "0.00", "13,068,955.00", "3,036.00"]
    }
    st.table(pd.DataFrame(data))
    st.markdown("</div>", unsafe_allow_html=True)

# --- العمود الأيسر (التحذيرات وتلميح اليوم) ---
with col_left:
    st.markdown("""<div class='mizan-panel'><span class='panel-title'>⚠️ التحذيرات</span>
    <p style='font-size:12px; color:red;'>إن آخر عملية نسخ احتياطي مجدولة تمت في 06/25/2023</p>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class='mizan-panel' style='border-top-color: #27ae60;'><span class='panel-title' style='background-color:#27ae60;'>💡 تلميح اليوم</span>
    <p style='font-size:13px;'>يمكنك إخفاء بعض الحقول التي لا تحتاجها من خلال صفحة 'ميزات البرنامج' في الإعدادات.</p>
    </div>""", unsafe_allow_html=True)

# شريط الحالة السفلي (Footer)
st.markdown("""
    <div style='position: fixed; bottom: 0; left: 0; width: 100%; background-color: #2c3e50; color: white; padding: 5px; text-align: center; font-size: 12px;'>
        المستخدم الحالي: مسؤول النظام | الفرع الرئيسي | 2026-03-24
    </div>
    """, unsafe_allow_html=True)
