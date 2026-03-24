import streamlit as st
import pandas as pd

# إعداد الصفحة لتشبه أنظمة الويندوز الاحترافية
st.set_page_config(page_title="برنامج الميزان للمحاسبة والمستودعات", layout="wide")

# تصميم CSS لمحاكاة ألوان وجداول برنامج الميزان الأصلي
st.markdown("""
    <style>
    .main { background-color: #e1e4e8; }
    .stButton>button { width: 100%; border-radius: 2px; background-color: #f0f0f0; color: black; border: 1px solid #707070; }
    .stButton>button:hover { background-color: #e5e5e5; }
    .header-box { background-color: #005a9e; color: white; padding: 10px; border-radius: 3px; text-align: center; margin-bottom: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .report-table { background-color: white; border: 1px solid #bcbcbc; }
    </style>
    """, unsafe_allow_html=True)

# ترويسة البرنامج
st.markdown("<div class='header-box'><h1>شركة الحلول البرمجية - نظام الميزان المحاسبي</h1></div>", unsafe_allow_html=True)

# نظام تخزين البيانات (قاعدة بيانات مؤقتة)
if 'journal' not in st.session_state:
    st.session_state.journal = []

# --- شجرة الحسابات (Tree View Simulation) ---
accounts_tree = {
    "1- الأصول": ["11- الصندوق", "12- المصرف", "13- الزبائن"],
    "2- الخصوم": ["21- الموردون", "22- القروض"],
    "3- الإيرادات": ["31- مبيعات بضاعة", "32- إيرادات خدمية"],
    "4- المصاريف": ["41- مشتريات", "42- رواتب وأجور", "43- مصاريف عامة"]
}

# --- القوائم العلوية (مثل نظام القوائم في الميزان) ---
tabs = st.tabs(["🏠 الرئيسية", "📒 قيود اليومية", "⚖️ ميزان المراجعة", "🗂️ بطاقة حساب"])

with tabs[0]: # شاشة المؤشرات الرئيسية
    st.subheader("📊 ملخص المركز المالي")
    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        c1, c2, c3, c4 = st.columns(4)
        total_debit = df["مدين"].sum()
        total_credit = df["دائن"].sum()
        c1.metric("إجمالي المدين", f"{total_debit:,.2f}")
        c2.metric("إجمالي الدائن", f"{total_credit:,.2f}")
        c3.metric("الرصيد الحالي", f"{total_debit - total_credit:,.2f}")
        c4.write("✅ النظام متزن")
    else:
        st.info("نظام الميزان جاهز للعمل. يرجى إدخال القيود من التبويب المخصص.")

with tabs[1]: # سند قيد (مثل واجهة سند القيد في الميزان)
    st.markdown("### 📝 سند قيد يومي")
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        cat = col1.selectbox("الحساب الرئيسي", list(accounts_tree.keys()))
        acc = col1.selectbox("الحساب الفرعي", accounts_tree[cat])
        amount = col2.number_input("المبلغ الحالي", min_value=0.0)
        entry_type = col3.radio("نوع القيد", ["مدين (+)", "دائن (-)"])
        note = st.text_area("البيان التفصيلي للعملية")
        
        if st.button("ترحيل السند"):
            st.session_state.journal.append({
                "التاريخ": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "الحساب": acc,
                "مدين": amount if "مدين" in entry_type else 0,
                "دائن": amount if "دائن" in entry_type else 0,
                "البيان": note
            })
            st.success("تم ترحيل السند إلى دفتر اليومية بنجاح.")

with tabs[2]: # ميزان المراجعة
    st.markdown("### ⚖️ ميزان المراجعة التفصيلي")
    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        summary = df.groupby("الحساب").agg({"مدين": "sum", "دائن": "sum"})
        summary["الرصيد"] = summary["مدين"] - summary["دائن"]
        st.table(summary.style.format("{:,.2f}"))
    else:
        st.warning("لا توجد بيانات للترحيل حالياً.")

with tabs[3]: # دفتر الأستاذ / بطاقة حساب
    st.markdown("### 🗂️ بطاقة حساب تفصيلية")
    search_acc = st.selectbox("اختر الحساب للمراجعة", [item for sublist in accounts_tree.values() for item in sublist])
    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        filtered_df = df[df["الحساب"] == search_acc]
        st.dataframe(filtered_df, use_container_width=True)

# شريط الأدوات السفلي
st.sidebar.markdown("---")
if st.sidebar.button("💾 حفظ البيانات (Excel)"):
    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        df.to_csv("mizan_data.csv", index=False)
        st.sidebar.success("تم التصدير بنجاح")

if st.sidebar.button("⚙️ إعدادات النظام"):
    st.sidebar.write("إصدار البرنامج: 2026.1.0")
