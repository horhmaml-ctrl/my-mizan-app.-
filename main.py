import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="النظام المتكامل", layout="centered", initial_sidebar_state="collapsed")

# تصميم CSS لإجبار العناصر على التنسيق الشبكي (Grid) مثل التطبيقات
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding: 0px !important; }
    .stApp { background-color: #ffffff; }

    /* الشريط العلوي */
    .app-header {
        background-color: #2563eb; color: white; padding: 12px;
        display: flex; justify-content: space-between; align-items: center;
        font-weight: bold; position: sticky; top: 0; z-index: 1000;
    }

    /* شبكة الأزرار العلوية الصغيرة (3 أعمدة) */
    .quick-actions {
        display: grid; grid-template-columns: repeat(3, 1fr);
        gap: 5px; padding: 10px; background-color: #f1f5f9;
    }
    .action-btn {
        background-color: #3b82f6; color: white; border-radius: 5px;
        padding: 8px 2px; text-align: center; font-size: 10px; font-weight: bold;
    }

    /* شبكة البطاقات الرئيسية (2 عمود - متناسقة تماماً) */
    .main-grid {
        display: grid;
        grid-template-columns: 1fr 1fr; /* هذا ما يضمن وجود عمودين بجانب بعضهما */
        gap: 12px;
        padding: 15px;
        margin-bottom: 60px;
    }
    .card {
        background: white;
        border: 1.5px solid #dbeafe;
        border-radius: 15px;
        padding: 20px 10px;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .card-icon { font-size: 40px; margin-bottom: 10px; }
    .card-title { font-size: 14px; font-weight: bold; color: #334155; margin: 0; }
    .card-count { color: #ef4444; font-size: 20px; font-weight: bold; margin-top: 5px; }

    /* الفوتر السفلي */
    .footer-status {
        position: fixed; bottom: 0; width: 100%;
        background-color: #1d4ed8; color: white;
        display: grid; grid-template-columns: repeat(3, 1fr);
        text-align: center; padding: 10px 0; font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Header
st.markdown("""
    <div class='app-header'>
        <span>🔍</span>
        <span>نظام محاسبي متكامل</span>
        <span>☰</span>
    </div>
    """, unsafe_allow_html=True)

# 2. Quick Actions (الأزرار الصغيرة)
# نستخدم HTML و CSS Grid لضمان التنسيق
st.markdown("""
    <div class='quick-actions'>
        <div class='action-btn' style='background-color:#2563eb;'>سند صرف/قبض</div>
        <div class='action-btn' style='background-color:#2563eb;'>سند جديد</div>
        <div class='action-btn' style='background-color:#2563eb;'>قيد عام</div>
        <div class='action-btn' style='background-color:#8b5cf6;'>فاتورة جديدة</div>
        <div class='action-btn' style='background-color:#8b5cf6;'>حوالة جديدة</div>
        <div class='action-btn' style='background-color:#8b5cf6;'>عروض/طلبيات</div>
        <div class='action-btn'>مراجعة الحركات</div>
        <div class='action-btn'>صرف عملات</div>
        <div class='action-btn'>كشف حساب</div>
    </div>
    """, unsafe_allow_html=True)

# 3. Main Dashboard Grid (البطاقات المتناسقة 2x2)
# هنا السر في التنسيق المتطابق مع الصورة
st.markdown("""
    <div class='main-grid'>
        <div class='card'>
            <div class='card-icon'>👤</div>
            <p class='card-title'>العملاء</p>
            <p class='card-count'>0</p>
        </div>
        <div class='card'>
            <div class='card-icon'>🚚</div>
            <p class='card-title'>الموردين</p>
            <p class='card-count'>0</p>
        </div>
        <div class='card'>
            <div class='card-icon'>🏢</div>
            <p class='card-title'>الموظفين</p>
            <p class='card-count'>0</p>
        </div>
        <div class='card'>
            <div class='card-icon'>✂️</div>
            <p class='card-title'>المصاريف</p>
            <p class='card-count'>0</p>
        </div>
        <div class='card'>
            <div class='card-icon'>📉</div>
            <p class='card-title'>المشتريات</p>
            <p class='card-count'>0</p>
        </div>
        <div class='card'>
            <div class='card-icon'>📈</div>
            <p class='card-title'>المبيعات</p>
            <p class='card-count'>0</p>
        </div>
        <div class='card'>
            <div class='card-icon'>🏦</div>
            <p class='card-title'>الصناديق والبنوك</p>
            <p class='card-count'>0</p>
        </div>
        <div class='card'>
            <div class='card-icon'>📜</div>
            <p class='card-title'>الاصول</p>
            <p class='card-count'>0</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. Fixed Footer
st.markdown("""
    <div class='footer-status'>
        <div>الإيرادات<br>0.00</div>
        <div>المصروفات<br>0.00</div>
        <div>صافي الأرباح<br>0.00</div>
    </div>
    """, unsafe_allow_html=True)
