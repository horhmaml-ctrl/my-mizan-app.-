import streamlit as st
import pandas as pd

# إعداد واجهة التطبيق
st.set_page_config(page_title="الميزان الاحترافي", layout="wide")
st.markdown("<h2 style='text-align: center; color: #2E86C1; direction: rtl;'>🏢 نظام الميزان المحاسبي المتكامل</h2>", unsafe_allow_html=True)

# التأكد من وجود سجل البيانات في الجلسة الحالية
if 'journal' not in st.session_state:
    st.session_state.journal = []

# قائمة الحسابات الافتراضية
accounts = ["الصندوق", "البنك", "المبيعات", "المشتريات", "الرواتب", "الموردين", "الزبائن", "إيجار", "كهرباء"]

# القائمة الجانبية للتنقل
st.sidebar.markdown("### 🛠️ لوحة التحكم")
menu = st.sidebar.radio("انتقل إلى:", ["إضافة عملية جديدة", "دفتر اليومية العام", "كشف حساب تفصيلي", "ميزان المراجعة"])

# 1. شاشة إضافة العمليات
if menu == "إضافة عملية جديدة":
    st.info("قم بتسجيل العمليات المالية هنا")
    with st.form("entry_form"):
        c1, c2, c3 = st.columns(3)
        acc_name = c1.selectbox("الحساب المختص", accounts)
        debit = c2.number_input("مدين (+)", min_value=0.0, format="%.2f")
        credit = c3.number_input("دائن (-)", min_value=0.0, format="%.2f")
        note = st.text_input("وصف العملية (البيان)")
        
        if st.form_submit_button("حفظ في الدفاتر ✅"):
            st.session_state.journal.append({
                "التاريخ": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                "الحساب": acc_name, "مدين": debit, "دائن": credit, "البيان": note
            })
            st.success(f"تم تسجيل العملية بنجاح!")

# 2. شاشة ميزان المراجعة
elif menu == "ميزان المراجعة":
    st.subheader("⚖️ ميزان المراجعة الإجمالي")
    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        summary = df.groupby("الحساب").agg({"مدين": "sum", "دائن": "sum"})
        summary["الرصيد"] = summary["مدين"] - summary["دائن"]
        st.table(summary)
        st.write(f"**إجمالي الحركة:** مدين ({summary['مدين'].sum()}) | دائن ({summary['دائن'].sum()})")
    else: st.warning("لا توجد أرصدة لعرضها")

# 3. دفتر اليومية
elif menu == "دفتر اليومية العام":
    if st.session_state.journal:
        st.dataframe(pd.DataFrame(st.session_state.journal), use_container_width=True)
    else: st.info("الدفاتر فارغة")

# 4. كشف حساب تفصيلي
elif menu == "كشف حساب تفصيلي":
    target = st.selectbox("اختر الحساب", accounts)
    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        res = df[df["الحساب"] == target]
        st.table(res)
        st.metric("صافي رصيد الحساب", f"{res['مدين'].sum() - res['دائن'].sum()} $")

# زر الحذف الشامل
if st.sidebar.button("⚠️ إعادة ضبط النظام"):
    st.session_state.journal = []
    st.rerun()
