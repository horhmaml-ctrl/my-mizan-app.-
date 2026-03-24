import streamlit as st

# إعداد الصفحة كلياً
st.set_page_config(page_title="الميزان برو", layout="centered")

# تصميم CSS جبري (لا يسمح للمتصفح بتغيير التنسيق)
st.markdown("""
    <style>
    /* إخفاء كل زوائد الموقع */
    .block-container { padding: 0px !important; max-width: 100% !important; }
    footer, header, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f1f5f9; }

    /* هيدر التطبيق */
    .app-header {
        background-color: #2563eb; color: white; padding: 15px;
        text-align: center; font-weight: bold; font-size: 18px;
        position: sticky; top: 0; z-index: 100;
    }

    /* شبكة المربعات (Grid) - ثابتة عمودين */
    .custom-grid {
        display: grid;
        grid-template-columns: 1fr 1fr; /* عمودين فقط */
        gap: 10px;
        padding: 10px;
    }

    /* تصميم البطاقة كزر تفاعلي */
    .card-btn {
        background-color: white;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 20px 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .card-icon { font-size: 32px; margin-bottom: 5px; }
    .card-text { font-size: 14px; font-weight: bold; color: #334155; }
    .card-val { color: #ef4444; font-weight: bold; font-size: 16px; }

    /* فوتر ثابت */
    .status-footer {
        position: fixed; bottom: 0; width: 100%;
        background-color: #1e40af; color: white;
        display: grid; grid-template-columns: repeat(3, 1fr);
        text-align: center; padding: 10px 0; font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. الهيدر
st.markdown("<div class='app-header'>نظام محاسبي متكامل</div>", unsafe_allow_html=True)

# 2. الأزرار العلوية الصغيرة (باستخدام أعمدة Streamlit لأنها بسيطة هنا)
c1, c2, c3 = st.columns(3)
with c1: st.button("📄 سندات")
with c2: st.button("➕ فاتورة")
with c3: st.button("🔍 بحث")

# 3. بناء الشبكة المتناسقة يدوياً (هنا يكمن الحل)
# سنستخدم الـ HTML مباشرة لضمان التنسيق 2x2
st.markdown("""
    <div class='custom-grid'>
        <div class='card-btn'><span class='card-icon'>👤</span><span class='card-text'>العملاء</span><span class='card-val'>0</span></div>
        <div class='card-btn'><span class='card-icon'>🚚</span><span class='card-text'>الموردين</span><span class='card-val'>0</span></div>
        <div class='card-btn'><span class='card-icon'>📈</span><span class='card-text'>المبيعات</span><span class='card-val'>0</span></div>
        <div class='card-btn'><span class='card-icon'>📉</span><span class='card-text'>المشتريات</span><span class='card-val'>0</span></div>
        <div class='card-btn'><span class='card-icon'>✂️</span><span class='card-text'>المصاريف</span><span class='card-val'>0</span></div>
        <div class='card-btn'><span class='card-icon'>🏢</span><span class='card-text'>الموظفين</span><span class='card-val'>0</span></div>
        <div class='card-btn'><span class='card-icon'>🏦</span><span class='card-text'>الصناديق</span><span class='card-val'>0</span></div>
        <div class='card-btn'><span class='card-icon'>📂</span><span class='card-text'>الأصول</span><span class='card-val'>0</span></div>
    </div>
    <div style='height: 60px;'></div>
    <div class='status-footer'>
        <div>الإيرادات<br>0.00</div>
        <div>المصروفات<br>0.00</div>
        <div>الأرباح<br>0.00</div>
    </div>
    """, unsafe_allow_html=True)
