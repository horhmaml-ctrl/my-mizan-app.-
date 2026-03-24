import streamlit as st
import pandas as pd

# إعدادات الصفحة - واجهة عريضة
st.set_page_config(page_title="المحاسبة التجارية Pro", layout="wide", initial_sidebar_state="expanded")

# تصميم CSS متقدم لمحاكاة تطبيقات المحاسبة التجارية (اللون البرتقالي والرمادي الاحترافي)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stSidebar"] { background-color: #262730; color: white; }
    .stMetric { background-color: white; padding: 20px; border-radius: 10px; border-right: 5px solid #FF8C00; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .btn-box { background-color: #FF8C00; color: white; padding: 10px; border-radius: 5px; text-align: center; cursor: pointer; margin: 5px; font-weight: bold; }
    .account-tree { font-family: 'Segoe UI'; font-size: 14px; color: #FF8C00; }
    div.stButton > button { background-color: #FF8C00; color: white; border-radius: 5px; width: 100%; height: 3em; border: none; font-weight: bold; }
    div.stButton > button:hover { background-color: #e67e00; border: none; }
    </style>
    """, unsafe_allow_html=True)

# بيانات الجلسة
if 'journal' not in st.session_state:
    st.session_state.journal = []

# --- شجرة الحسابات الدائمة في القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #FF8C00;'>🌳 شجرة الحسابات</h2>", unsafe_allow_html=True)
    with st.expander("📂 1- الأصول (الموجودات)"):
        st.write("📄 1101- الصندوق الرئيسي")
        st.write("📄 1102- بنك البلاد")
        st.write("📄 1201- مخزون المستودع")
    with st.expander("📂 2- الخصوم (المطاليب)"):
        st.write("📄 2101- شركة التوريدات")
        st.write("📄 2201- ذمم دائنة")
    with st.expander("📂 3- الإيرادات"):
        st.write("📄 3101- مبيعات نقدية")
        st.write("📄 3102- مبيعات آجلة")
    with st.expander("📂 4- المصاريف"):
        st.write("📄 4101- مشتريات بضاعة")
        st.write("📄 4201- إيجارات ورواتب")
    st.markdown("---")
    st.info("نظام المحاسبة التجارية - الإصدار 2.0")

# --- الواجهة الرئيسية (الواجهة التي طلبتها) ---
st.markdown("<h1 style='text-align: right; color: #262730;'>📊 لوحة تحكم المحاسبة التجارية</h1>", unsafe_allow_html=True)

# 1. صناديق الحالة السريعة (Top Metrics)
if st.session_state.journal:
    df = pd.DataFrame(st.session_state.journal)
    rev = df[df["النوع"] == "إيراد"]["المبلغ"].sum()
    exp = df[df["النوع"] == "مصروف"]["المبلغ"].sum()
    bal = rev - exp
else:
    rev, exp, bal = 0, 0, 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 السيولة النقدية", f"{bal:,.2f}")
c2.metric("📈 إجمالي المبيعات", f"{rev:,.2f}")
c3.metric("📉 إجمالي المصاريف", f"{exp:,.2f}")
c4.metric("⚖️ صافي الربح", f"{bal:,.2f}", delta=float(bal))

st.markdown("---")

# 2. منطقة العمليات الرئيسية (مثل أزرار التطبيق الفعلي)
col_a, col_b = st.columns([1, 2])

with col_a:
    st.markdown("### ⚡ عمليات سريعة")
    op = st.radio("اختر العملية:", ["➕ فاتورة مبيعات", "➖ سند صرف مصروف", "🔄 قيد يومية", "📑 كشف حساب"])
    
with col_b:
    if "فاتورة مبيعات" in op:
        st.subheader("📝 إنشاء فاتورة مبيعات جديدة")
        with st.form("sale_form"):
            acc = st.selectbox("إلى حساب (الزبون/الصندوق)", ["1101- الصندوق الرئيسي", "3101- مبيعات نقدية"])
            amt = st.number_input("قيمة الفاتورة", min_value=0.0)
            note = st.text_input("ملاحظات الفاتورة")
            if st.form_submit_button("اعتماد وحفظ الفاتورة"):
                st.session_state.journal.append({"التاريخ": pd.Timestamp.now().strftime("%Y-%m-%d"), "الحساب": acc, "المبلغ": amt, "النوع": "إيراد", "البيان": note})
                st.success("تم الحفظ!")

    elif "سند صرف" in op:
        st.subheader("💸 سند صرف مصروفات")
        with st.form("exp_form"):
            acc = st.selectbox("من حساب (المصروفات)", ["4101- مشتريات بضاعة", "4201- إيجارات ورواتب"])
            amt = st.number_input("المبلغ المدفوع", min_value=0.0)
            note = st.text_input("بيان الصرف")
            if st.form_submit_button("تأكيد الصرف"):
                st.session_state.journal.append({"التاريخ": pd.Timestamp.now().strftime("%Y-%m-%d"), "الحساب": acc, "المبلغ": amt, "النوع": "مصروف", "البيان": note})
                st.success("تم الصرف!")

# 3. جدول البيانات السفلي (مثل شاشة عرض القيود في التطبيق)
st.markdown("### 🔍 سجل العمليات الأخيرة")
if st.session_state.journal:
    st.table(pd.DataFrame(st.session_state.journal).tail(10))
else:
    st.write("لا توجد عمليات مسجلة اليوم.")

# تذييل الصفحة
st.sidebar.button("💾 حفظ البيانات (Cloud Backup)")
