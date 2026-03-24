import streamlit as st
import pandas as pd

# إعدادات واجهة تشبه البرامج المؤسسية
st.set_page_config(page_title="نظام الميزان المحاسبي Pro", layout="wide")

# تزيين الواجهة برأس احترافي
st.markdown("""
    <div style='background-color: #2c3e50; padding: 20px; border-radius: 10px; margin-bottom: 25px;'>
        <h1 style='color: white; text-align: center; margin: 0;'>📊 نظام الميزان المحاسبي الذكي</h1>
        <p style='color: #bdc3c7; text-align: center;'>الإصدار الاحترافي v1.0</p>
    </div>
""", unsafe_allow_html=True)

if 'journal' not in st.session_state:
    st.session_state.journal = []

# دليل الحسابات المصنف
account_categories = {
    "الأصول (أموالك)": ["الصندوق", "البنك", "المخزون"],
    "المصاريف": ["رواتب", "إيجار", "كهرباء", "مشتريات"],
    "الإيرادات": ["المبيعات", "إيرادات أخرى"],
    "الالتزامات": ["الموردين", "قروض"]
}

# القائمة الجانبية
st.sidebar.title("💳 القائمة الرئيسية")
menu = st.sidebar.radio("انتقل إلى:", ["لوحة التحكم (Dashboard)", "إضافة قيد محاسبي", "دفتر اليومية العام", "ميزان المراجعة"])

df = pd.DataFrame(st.session_state.journal) if st.session_state.journal else pd.DataFrame(columns=["التاريخ", "الحساب", "التصنيف", "مدين", "دائن", "البيان"])

if menu == "لوحة التحكم (Dashboard)":
    st.subheader("📈 الملخص المالي اللحظي")
    if not df.empty:
        # حسابات سريعة
        total_debit = df["مدين"].sum()
        total_credit = df["دائن"].sum()
        revenue = df[df["التصنيف"] == "الإيرادات"]["دائن"].sum()
        expenses = df[df["التصنيف"] == "المصاريف"]["مدين"].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي الإيرادات", f"{revenue} $")
        c2.metric("إجمالي المصاريف", f"{expenses} $")
        c3.metric("صافي الربح", f"{revenue - expenses} $", delta=float(revenue - expenses))
        
        st.divider()
        st.subheader("📊 تحليل الحسابات")
        st.bar_chart(df.groupby("الحساب")[["مدين", "دائن"]].sum())
    else:
        st.info("ابدأ بإضافة أول قيد محاسبي لتظهر الإحصائيات هنا.")

elif menu == "إضافة قيد محاسبي":
    st.subheader("📝 تسجيل حركة مالية")
    with st.form("accounting_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        cat = col1.selectbox("فئة الحساب", list(account_categories.keys()))
        acc = col2.selectbox("اسم الحساب", account_categories[cat])
        
        col3, col4 = st.columns(2)
        debit = col3.number_input("مدين (إدخال مبلغ +)", min_value=0.0)
        credit = col4.number_input("دائن (إخراج مبلغ -)", min_value=0.0)
        
        note = st.text_input("البيان (شرح العملية)")
        
        if st.form_submit_button("ترحيل العملية إلى الميزانية ✅"):
            st.session_state.journal.append({
                "التاريخ": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "الحساب": acc, "التصنيف": cat, "مدين": debit, "دائن": credit, "البيان": note
            })
            st.success("تم ترحيل القيد بنجاح!")

elif menu == "ميزان المراجعة":
    st.subheader("⚖️ ميزان المراجعة التحليلي")
    if not df.empty:
        summary = df.groupby(["التصنيف", "الحساب"]).agg({"مدين": "sum", "دائن": "sum"})
        summary["الرصيد"] = summary["مدين"] - summary["دائن"]
        st.table(summary)
    else: st.warning("لا توجد أرصدة")

if st.sidebar.button("🗑️ تصفير النظام"):
    st.session_state.journal = []
    st.rerun()
