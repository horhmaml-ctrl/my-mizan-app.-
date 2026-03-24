import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات النظام الكبرى
st.set_page_config(page_title="الخوارزمي للمحاسبة والمستودعات", layout="wide")

# 2. محرك قاعدة البيانات (Core Engine)
if 'mizan_engine' not in st.session_state:
    st.session_state.mizan_engine = {
        'journal': pd.DataFrame(columns=['رقم_السند', 'التاريخ', 'الحساب', 'مدين', 'دائن', 'البيان']),
        'inventory': {'صنف_أ': 100, 'صنف_ب': 200},
        'accounts': {
            '101': {'name': 'الصندوق الرئيسي', 'bal': 380500.00},
            '102': {'name': 'صندوق العملات', 'bal': 0.00},
            '103': {'name': 'صرافة السنيري', 'bal': 13068955.00}
        }
    }

# 3. واجهة المستخدم (محاكاة الميزان دوت نت 100%)
st.markdown("""
    <style>
    .stApp { background-color: #f4f6f9; }
    .header-mizan { background: linear-gradient(90deg, #d35400, #e67e22); color: white; padding: 10px 20px; border-bottom: 2px solid #a04000; display: flex; justify-content: space-between; }
    .mizan-panel { background: white; border: 1px solid #d1d5db; border-radius: 4px; margin-bottom: 10px; }
    .mizan-panel-title { background: #34495e; color: white; padding: 5px 10px; font-size: 14px; text-align: right; }
    .mizan-panel-body { padding: 15px; }
    div.stButton > button { width: 100%; border-radius: 4px; text-align: right; background: #f8fafc; border: 1px solid #cbd5e1; }
    </style>
    """, unsafe_allow_html=True)

# الهيدر العلوي
st.markdown("<div class='header-mizan'><div><b>الخوارزمي دوت نت</b> للمحاسبة والمستودعات</div><div>المسؤول: ABO OMER2026</div></div>", unsafe_allow_html=True)

# تقسيم الشاشة (كما في الصورة)
col_info, col_actions, col_status = st.columns([1.2, 1, 1.2])

with col_info:
    # لوحة التحذيرات
    st.markdown("<div class='mizan-panel'><div class='mizan-panel-title'>⛔ التحذيرات</div><div class='mizan-panel-body' style='color:red;'>آخر نسخة احتياطية: 2026/03/24</div></div>", unsafe_allow_html=True)
    # لوحة تلميح اليوم
    st.markdown("<div class='mizan-panel'><div class='mizan-panel-title'>💡 تلميح اليوم</div><div class='mizan-panel-body'>استخدم اختصار F2 لحفظ الفواتير بسرعة.</div></div>", unsafe_allow_html=True)

with col_actions:
    # قائمة الاختصارات (أهم العمليات)
    st.markdown("<div class='mizan-panel'><div class='mizan-panel-title'>🔗 الاختصارات الرئيسية</div><div class='mizan-panel-body'>", unsafe_allow_html=True)
    if st.button("📄 فاتورة مبيع آجل"): pass
    if st.button("💸 سند صرف نقدي"): pass
    if st.button("📦 إدخال بضاعة جاهزة"): pass
    if st.button("👤 أرصدة العملاء"): pass
    st.markdown("</div></div>", unsafe_allow_html=True)

with col_status:
    # الوقت والأرصدة
    now = datetime.now()
    st.markdown(f"<h1 style='text-align:right; color:#2c3e50;'>{now.strftime('%H:%M')}</h1>", unsafe_allow_html=True)
    st.markdown("<div class='mizan-panel'><div class='mizan-panel-title'>🏦 أرصدة الحسابات الجارية</div><div class='mizan-panel-body'>", unsafe_allow_html=True)
    for code, info in st.session_state.mizan_engine['accounts'].items():
        st.write(f"**{info['name']}:** {info['bal']:,.2f}")
    st.markdown("</div></div>", unsafe_allow_html=True)

# ميكانيكا النظام (الترحيل الآلي)
st.write("---")
with st.expander("📝 إضافة قيد محاسبي سريع (محاكاة الترحيل)"):
    acc = st.selectbox("الحساب", ["الصندوق الرئيسي", "صرافة السنيري"])
    amt = st.number_input("المبلغ", min_value=0.0)
    if st.button("ترحيل القيد ✅"):
        st.success(f"تم ترحيل مبلغ {amt} إلى {acc} وتحديث ميزان المراجعة فوراً.")
