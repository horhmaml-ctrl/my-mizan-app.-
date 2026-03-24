import streamlit as st
import pandas as pd
import plotly.express as px # لإضافة رسوم بيانية

st.set_page_config(page_title="نظام الميزان المحاسبي", layout="wide")

# تصميم الواجهة بالألوان الاحترافية
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

if 'journal' not in st.session_state:
    st.session_state.journal = []

# --- القائمة الجانبية ---
st.sidebar.title("📊 الميزان Pro")
menu = st.sidebar.selectbox("القائمة الرئيسية", ["الرئيسية (Dashboard)", "إدخال قيود", "دفتر اليومية", "كشف حساب"])

# بيانات وهمية للبدء إذا كان الدفتر فارغاً (اختياري)
df = pd.DataFrame(st.session_state.journal) if st.session_state.journal else pd.DataFrame(columns=["التاريخ", "الحساب", "مدين", "دائن", "البيان"])

if menu == "الرئيسية (Dashboard)":
    st.title("📈 لوحة التحكم المالية")
    
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        total_in = df["مدين"].sum()
        total_out = df["دائن"].sum()
        col1.metric("إجمالي المقبوضات", f"{total_in} $")
        col2.metric("إجمالي المصاريف", f"{total_out} $")
        col3.metric("صافي الربح", f"{total_in - total_out} $", delta=float(total_in - total_out))

        # رسم بياني للمصاريف
        st.subheader("📊 تحليل الحسابات")
        chart_data = df.groupby("الحساب")[["مدين", "دائن"]].sum()
        st.bar_chart(chart_data)
    else:
        st.info("مرحباً بك! ابدأ بإدخال أول عملية مالية من القائمة الجانبية.")

elif menu == "إدخال قيود":
    st.subheader("📝 تسجيل قيد محاسبي جديد")
    with st.form("my_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        acc = c1.selectbox("اسم الحساب", ["الصندوق", "البنك", "المبيعات", "المشتريات", "رواتب", "إيجار"])
        amount_type = c2.radio("نوع العملية", ["قبض (مدين)", "صرف (دائن)"])
        amount = st.number_input("المبلغ", min_value=0.0)
        note = st.text_input("البيان / ملاحظات")
        
        if st.form_submit_button("اعتماد القيد"):
            new_entry = {
                "التاريخ": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "الحساب": acc,
                "مدين": amount if "قبض" in amount_type else 0,
                "دائن": amount if "صرف" in amount_type else 0,
                "البيان": note
            }
            st.session_state.journal.append(new_entry)
            st.success("تم ترحيل القيد للميزانية!")

elif menu == "دفتر اليومية":
    st.subheader("📅 سجل العمليات اليومية")
    st.dataframe(df, use_container_width=True)

# زر الحذف
if st.sidebar.button("⚠️ تصفير النظام"):
    st.session_state.journal = []
    st.rerun()
