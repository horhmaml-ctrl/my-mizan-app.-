import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة لتكون واسعة جداً مثل برامج الكمبيوتر
st.set_page_config(page_title="الخوارزمي - نظام المحاسبة والمستودعات", layout="wide")

# --- محاكي قاعدة البيانات (Database) ---
if 'ledger' not in st.session_state:
    st.session_state.ledger = pd.DataFrame(columns=['التاريخ', 'الحساب', 'مدين', 'دائن', 'البيان'])
    st.session_state.balances = {"صندوق": 380500.00, "صندوق العملات": 0.00, "صرافة السنيري": 13068955.00}

# --- التصميم الاحترافي (نفس ألوان الميزان في الصورة) ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    /* الهيدر العلوي */
    .top-header { background: #e67e22; color: white; padding: 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #d35400; }
    /* كتل المعلومات (الاختصارات، الحسابات) */
    .mizan-block { background: white; border: 1px solid #bdc3c7; border-radius: 4px; margin-bottom: 10px; }
    .mizan-block-title { background: #34495e; color: white; padding: 5px 10px; font-size: 14px; font-weight: bold; text-align: right; }
    .mizan-content { padding: 10px; font-size: 13px; }
    /* الساعة الكبيرة */
    .big-clock { color: #2c3e50; font-size: 48px; font-weight: bold; text-align: right; margin: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- الهيدر (الخوارزمي دوت نت) ---
st.markdown("""
    <div class='top-header'>
        <div>الخوارزمي دوت نت<br><small>للمحاسبة والمستودعات</small></div>
        <div style='text-align:left;'>مسؤول النظام<br><small>ABO OMER2026</small></div>
    </div>
    """, unsafe_allow_html=True)

# --- الواجهة الرئيسية (محاكاة الصورة 100%) ---
col_left, col_mid, col_right = st.columns([1, 1, 1])

with col_left:
    # بلوك التحذيرات
    st.markdown("<div class='mizan-block'><div class='mizan-block-title'>⛔ التحذيرات</div><div class='mizan-content' style='color:red;'>إن آخر عملية نسخ احتياطي محولة تمت في: 2026/03/24</div></div>", unsafe_allow_html=True)
    # بلوك تلميح اليوم
    st.markdown("<div class='mizan-block'><div class='mizan-block-title'>💡 تلميح اليوم</div><div class='mizan-content'>يمكنك إخفاء بعض الحقول التي لا تحتاجها عبر قائمة 'خيارات البرنامج'.</div></div>", unsafe_allow_html=True)

with col_mid:
    # بلوك الاختصارات (أساس العمل)
    st.markdown("<div class='mizan-block'><div class='mizan-block-title'>🔗 الاختصارات</div><div class='mizan-content'>", unsafe_allow_html=True)
    if st.button("📄 فاتورة مبيع آجل"): pass
    if st.button("💸 سند صرف"): pass
    if st.button("📥 إدخال بضاعة جاهزة"): pass
    if st.button("💰 أرصدة العملاء"): pass
    st.markdown("</div></div>", unsafe_allow_html=True)

with col_right:
    # الساعة والتاريخ (كما في الصورة)
    now = datetime.now()
    st.markdown(f"<div class='big-clock'>{now.strftime('%H:%M')}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:right;'>{now.strftime('%B %d, %A')}</p>", unsafe_allow_html=True)
    
    # بلوك الحسابات (الأرصدة الحقيقية)
    st.markdown("<div class='mizan-block'><div class='mizan-block-title'>🏦 الحسابات</div><div class='mizan-content'>", unsafe_allow_html=True)
    for acc, bal in st.session_state.balances.items():
        st.write(f"**{acc}:** {bal:,.2f} ريال")
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- شريط الأدوات السفلي ---
st.markdown("---")
st.subheader("📑 القيود المحاسبية الأخيرة (دفتر اليومية)")
st.dataframe(st.session_state.ledger, use_container_width=True)
