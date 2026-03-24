import streamlit as st

# إعدادات الصفحة لتكون تطبيق جوال (بدون هوامش)
st.set_page_config(page_title="نظام محاسبي", layout="centered", initial_sidebar_state="collapsed")

# تصميم CSS مكثف لمحاكاة واجهة الأندرويد المحاسبية
st.markdown("""
    <style>
    /* إخفاء عناصر الويب */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding: 0px !important; margin: 0px !important; }
    .stApp { background-color: #f8fafc; }

    /* الشريط العلوي الأزرق الداكن */
    .app-header {
        background-color: #2563eb; color: white;
        padding: 15px; text-align: center;
        font-weight: bold; font-size: 18px;
        display: flex; justify-content: space-between;
        position: sticky; top: 0; z-index: 999;
    }

    /* شبكة الأزرار العلوية الصغيرة */
    .quick-grid {
        display: grid; grid-template-columns: repeat(3, 1fr);
        gap: 4px; padding: 5px; background: #e2e8f0;
    }
    div.stButton > button {
        width: 100%; height: 40px !important;
        background-color: #3b82f6; color: white;
        border: none; font-size: 11px; font-weight: bold;
        border-radius: 4px; padding: 0px;
    }
    /* أزرار بلون مختلف (بنفسجي/رمادي) حسب الصورة */
    div.stButton > button[kind="secondary"] { background-color: #6366f1; }

    /* تصميم البطاقات (Cards) */
    .card-container {
        display: grid; grid-template-columns: 1fr 1fr;
        gap: 10px; padding: 10px; margin-bottom: 60px;
    }
    .mizan-card {
        background: white; border: 1px solid #bfdbfe;
        border-radius: 12px; padding: 15px;
        text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .card-icon { width: 45px; margin-bottom: 8px; }
    .card-title { font-size: 14px; font-weight: bold; color: #1e293b; margin: 0; }
    .card-badge { color: #ef4444; font-size: 18px; font-weight: bold; }

    /* شريط المعلومات السفلي */
    .bottom-status-bar {
        position: fixed; bottom: 0; width: 100%;
        background-color: #1d4ed8; color: white;
        display: grid; grid-template-columns: 1fr 1fr 1fr;
        text-align: center; padding: 8px 0; font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Header
st.markdown("""
    <div class='app-header'>
        <span>🔍</span>
        <span>نظام محاسبي متكامل</span>
        <span>🌙 ☰</span>
    </div>
    """, unsafe_allow_html=True)

# 2. Quick Actions Row (الأزرار الصغيرة العلوية)
c1, c2, c3 = st.columns(3)
with c1: st.button("سند صرف/قبض")
with c2: st.button("سند جديد")
with c3: st.button("قيد عام")

c4, c5, c6 = st.columns(3)
with c4: st.button("فاتورة جديدة")
with c5: st.button("حوالة جديدة")
with c6: st.button("عروض/طلبيات")

c7, c8, c9 = st.columns(3)
with c7: st.button("مراجعة الحركات")
with c8: st.button("صرف عملات")
with c9: st.button("كشف حساب")

# 3. Dashboard Cards (البطاقات الرئيسية)
# سنستخدم الروابط المباشرة للأيقونات لتبدو حقيقية
cards = [
    {"title": "العملاء", "icon": "👤", "count": "0", "color": "#facc15"},
    {"title": "الموردين", "icon": "👨‍🔧", "count": "0", "color": "#3b82f6"},
    {"title": "المصاريف", "icon": "✂️", "count": "0", "color": "#22c55e"},
    {"title": "الموظفين", "icon": "🏢", "count": "0", "color": "#6366f1"},
    {"title": "المبيعات", "icon": "📈", "count": "0", "color": "#f97316"},
    {"title": "المشتريات", "icon": "🛒", "count": "0", "color": "#06b6d4"},
    {"title": "الاصول", "icon": "📜", "count": "0", "color": "#8b5cf6"},
    {"title": "الصناديق والبنوك", "icon": "🏦", "count": "0", "color": "#1e40af"}
]

# عرض البطاقات في صفوف (2 في كل صف)
for i in range(0, len(cards), 2):
    col_l, col_r = st.columns(2)
    with col_r: # اليمين في الصورة يبدأ بالعملاء
        card = cards[i]
        st.markdown(f"""
            <div class='mizan-card'>
                <div style='font-size:35px;'>{card['icon']}</div>
                <p class='card-title'>{card['title']}</p>
                <p class='card-badge'>{card['count']}</p>
            </div>
            """, unsafe_allow_html=True)
    with col_l:
        if i+1 < len(cards):
            card = cards[i+1]
            st.markdown(f"""
                <div class='mizan-card'>
                    <div style='font-size:35px;'>{card['icon']}</div>
                    <p class='card-title'>{card['title']}</p>
                    <p class='card-badge'>{card['count']}</p>
                </div>
                """, unsafe_allow_html=True)

# 4. Fixed Footer
st.markdown("""
    <div class='bottom-status-bar'>
        <div>الإيرادات<br>0.00</div>
        <div>المصروفات<br>0.00</div>
        <div>صافي الأرباح<br>0.00</div>
    </div>
    """, unsafe_allow_html=True)
