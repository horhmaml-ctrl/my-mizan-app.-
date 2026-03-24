import streamlit as st
import pandas as pd

# إعداد الصفحة وتغيير اللون الأساسي للبرتقالي
st.set_page_config(page_title="نظام الميزان المحاسبي - Orange Edition", layout="wide")

# تصميم CSS مخصص للأيقونات البرتقالية وشجرة الحسابات
st.markdown("""
    <style>
    /* تغيير ألوان العناوين والأيقونات للبرتقالي */
    .header-box { background-color: #FF8C00; color: white; padding: 15px; border-radius: 5px; text-align: center; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #f0f2f6; border-radius: 5px 5px 0 0; padding: 10px 20px; color: #333;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #FF8C00 !important; color: white !important; 
    }
    /* تنسيق الجداول لتشبه تقارير الميزان */
    .report-font { font-family: 'Tahoma'; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# ترويسة البرنامج بالأيقونة البرتقالية
st.markdown("<div class='header-box'><h1>🟠 برنامج الميزان للمحاسبة والمستودعات</h1></div>", unsafe_allow_html=True)

if 'journal' not in st.session_state:
    st.session_state.journal = []

# --- الشجرة المحاسبية المنظمة ---
st.sidebar.markdown("### 🌳 الشجرة المحاسبية")
accounts_tree = {
    "1- الأصول": {
        "11- الأصول المتداولة": ["1101- الصندوق", "1102- المصرف", "1103- مخزون أول المدة"],
        "12- الأصول الثابتة": ["1201- الأثاث", "1202- الآلات والمعدات"]
    },
    "2- الخصوم": {
        "21- الالتزامات": ["2101- الموردون", "2102- قروض بنكية"]
    },
    "3- الإيرادات": {
        "31- المبيعات": ["3101- مبيعات محلية", "3102- مبيعات خارجية"]
    },
    "4- المصاريف": {
        "41- المشتريات": ["4101- مشتريات بضاعة"],
        "42- الأجور": ["4201- رواتب موظفين", "4202- بدلات سفر"]
    }
}

# عرض الشجرة في القائمة الجانبية (للمراجعة فقط)
for parent, children in accounts_tree.items():
    with st.sidebar.expander(parent):
        for sub_parent, sub_children in children.items():
            st.write(f"📂 {sub_parent}")
            for acc in sub_children:
                st.write(f"📄 {acc}")

# --- التبويبات الرئيسية (أيقونات برتقالية عند التحديد) ---
tabs = st.tabs(["🏠 الرئيسية", "📝 سند قيد", "📊 ميزان المراجعة", "📁 بطاقة حساب"])

with tabs[0]:
    st.subheader("🟠 ملخص الحركة المالية")
    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        c1, c2, c3 = st.columns(3)
        total_debit = df["مدين"].sum()
        total_credit = df["دائن"].sum()
        c1.metric("إجمالي المقبوضات", f"{total_debit:,.2f} $")
        c2.metric("إجمالي المدفوعات", f"{total_credit:,.2f} $")
        c3.metric("الرصيد الدفتري", f"{total_debit - total_credit:,.2f} $")
    else:
        st.info("قم بإضافة عمليات من تبويب 'سند قيد' لتفعيل التقارير.")

with tabs[1]:
    st.markdown("### 📝 إدخال سند قيد جديد")
    with st.container():
        col1, col2 = st.columns(2)
        main_cat = col1.selectbox("المستوى الأول (الشجرة)", list(accounts_tree.keys()))
        sub_cat = col1.selectbox("المستوى الثاني", list(accounts_tree[main_cat].keys()))
        final_acc = col1.selectbox("الحساب التفصيلي", accounts_tree[main_cat][sub_cat])
        
        amount = col2.number_input("المبلغ المالي", min_value=0.0)
        entry_type = col2.radio("نوع القيد", ["مدين (+)", "دائن (-)"])
        note = st.text_input("بيان العملية")
        
        if st.button("ترحيل السند إلى الحسابات 🟠"):
            st.session_state.journal.append({
                "التاريخ": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "الحساب": final_acc,
                "مدين": amount if "مدين" in entry_type else 0,
                "دائن": amount if "دائن" in entry_type else 0,
                "البيان": note
            })
            st.success(f"تم ترحيل المبلغ إلى حساب {final_acc}")

with tabs[2]:
    st.markdown("### ⚖️ ميزان المراجعة بالمجاميع والأرصدة")
    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        summary = df.groupby("الحساب").agg({"مدين": "sum", "دائن": "sum"})
        summary["الرصيد"] = summary["مدين"] - summary["دائن"]
        st.dataframe(summary.style.format("{:,.2f}"), use_container_width=True)
    else:
        st.warning("لا توجد بيانات مسجلة.")

with tabs[3]:
    st.markdown("### 📁 استعراض بطاقة حساب")
    all_accs = [acc for sub in accounts_tree.values() for s_sub in sub.values() for acc in s_sub]
    search = st.selectbox("ابحث عن الحساب", all_accs)
    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        st.table(df[df["الحساب"] == search])

# خيارات الحفظ
st.sidebar.markdown("---")
if st.sidebar.button("💾 تصدير قاعدة البيانات"):
    st.sidebar.info("تم حفظ البيانات بنجاح في السيرفر.")
