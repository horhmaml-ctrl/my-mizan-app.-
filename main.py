import streamlit as st

st.set_page_config(page_title="الميزان برو - الواجهة الكاملة", layout="centered")

# إدارة الصفحات
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# تصميم CSS احترافي للنصفين (العلوي والسفلي)
st.markdown("""
    <style>
    .block-container { padding: 0px !important; max-width: 100% !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f8fafc; }

    /* الهيدر */
    .app-header {
        background-color: #2563eb; color: white; padding: 12_px;
        text-align: center; font-weight: bold; font-size: 16px;
    }

    /* النصف العلوي: شبكة الأزرار السريعة (3 أعمدة) */
    .top-actions-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* 3 أعمدة متساوية دائماً */
        gap: 6px;
        padding: 10px;
        background-color: #e2e8f0;
    }
    
    /* تصميم أزرار العمليات السريعة */
    .action-item {
        background-color: #3b82f6; color: white;
        text-align: center; padding: 10px 2px;
        border-radius: 4px; font-size: 11px; font-weight: bold;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .action-item.alt { background-color: #6366f1; } /* لون مختلف لبعض الأزرار */

    /* النصف السفلي: شبكة البطاقات (2 عمود) */
    .bottom-cards-grid {
        display: grid;
        grid-template-columns: 1fr 1fr; /* عمودين فقط */
        gap: 12px;
        padding: 15px;
        margin-bottom: 70px;
    }
    .card {
        background: white; border-radius: 12px; padding: 15px;
        text-align: center; border: 1px solid #cbd5e1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .card-icon { font-size: 30px; }
    .card-title { font-size: 13px; font-weight: bold; color: #334155; margin-top: 5px; }
    .card-val { color: #ef4444; font-weight: bold; }

    /* الفوتر */
    .status-footer {
        position: fixed; bottom: 0; width: 100%;
        background-color: #1e40af; color: white;
        display: grid; grid-template-columns: repeat(3, 1fr);
        text-align: center; padding: 10px 0; font-size: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. الهيدر
st.markdown("<div class='app-header'>نظام محاسبي متكامل</div>", unsafe_allow_html=True)

# 2. النصف العلوي (أساس العمل - تم ضبطه ليكون 3 أعمدة)
st.markdown("""
    <div class='top-actions-grid'>
        <div class='action-item'>سند صرف/قبض</div>
        <div class='action-item'>سند جديد</div>
        <div class='action-item'>قيد عام</div>
        <div class='action-item' style='background-color:#8b5cf6;'>فاتورة جديدة</div>
        <div class='action-item' style='background-color:#8b5cf6;'>حوالة جديدة</div>
        <div class='action-item' style='background-color:#8b5cf6;'>عروض/طلبيات</div>
        <div class='action-item'>مراجعة الحركات</div>
        <div class='action-item'>صرف عملات</div>
        <div class='action-item'>كشف حساب</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# 3. النصف السفلي (البطاقات)
st.markdown("""
    <div class='bottom-cards-grid'>
        <div class='card'><div class='card-icon'>👤</div><div class='card-title'>العملاء</div><div class='card-val'>0</div></div>
        <div class='card'><div class='card-icon'>🚚</div><div class='card-title'>الموردين</div><div class='card-val'>0</div></div>
        <div class='card'><div class='card-icon'>📈</div><div class='card-title'>المبيعات</div><div class='card-val'>0</div></div>
        <div class='card'><div class='card-icon'>📉</div><div class='card-title'>المشتريات</div><div class='card-val'>0</div></div>
        <div class='card'><div class='card-icon'>✂️</div><div class='card-title'>المصاريف</div><div class='card-val'>0</div></div>
        <div class='card'><div class='card-icon'>🏢</div><div class='card-title'>الموظفين</div><div class='card-val'>0</div></div>
    </div>
    """, unsafe_allow_html=True)

# 4. الفوتر
st.markdown("""
    <div class='status-footer'>
        <div>الإيرادات<br>0.00</div>
        <div>المصروفات<br>0.00</div>
        <div>الأرباح<br>0.00</div>
    </div>
    """, unsafe_allow_html=True)

# زر تفاعلي حقيقي للانتقال لصفحة الفاتورة (للتجربة)
if st.button("🛠️ اضغط هنا لفتح واجهة الإدخال (التفاعلية)"):
    st.session_state.page = 'invoice'
    st.rerun()
