import streamlit as st
import pandas as pd

# إعداد الصفحة بنمط النظام المؤسسي
st.set_page_config(page_title="نظام الميزان المتكامل Pro", layout="wide")

# تصميم CSS للواجهة الاحترافية (أيقونات برتقالية وأزرار واضحة)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stSidebar { background-color: #2c3e50; }
    .module-card { background-color: white; padding: 20px; border-radius: 10px; border-top: 5px solid #FF8C00; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

# تهيئة مخازن البيانات (في تطبيق حقيقي نستخدم قاعدة بيانات)
if 'data' not in st.session_state:
    st.session_state.data = {
        'journal': [], 'inventory': {'مواد خام': 100, 'منتج جاهز': 0},
        'customers': ['عميل نقدي', 'شركة الأمل'], 'suppliers': ['مورد المواد', 'المصنع العالمي'],
        'employees': ['أحمد (محاسب)', 'سارّة (مبيعات)']
    }

# --- القائمة الجانبية: شجرة الحسابات المركزية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2622/2622814.png", width=100) # أيقونة برتقالية افتراضية
    st.markdown("<h2 style='color: #FF8C00;'>🏛️ مركز الإدارة</h2>", unsafe_allow_html=True)
    menu = st.radio("النشاط الحالي:", 
                    ["📊 لوحة القيادة", "📦 المستودعات", "🏭 خط التصنيع", "🧾 المشتريات (الموردين)", "💰 المبيعات (العملاء)", "👥 الموظفين", "⚖️ الحسابات الختامية"])

# --- 1. لوحة القيادة (Dashboard) ---
if menu == "📊 لوحة القيادة":
    st.title("📈 ملخص الأداء العام")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 قطع في المستودع", sum(st.session_state.data['inventory'].values()))
    c2.metric("👥 عدد العملاء", len(st.session_state.data['customers']))
    c3.metric("🏭 عمليات التصنيع", "5 جارية")
    c4.metric("💰 رصيد الصندوق", "15,400 $")
    
    st.markdown("### 🕒 آخر الحركات المالية")
    if st.session_state.data['journal']:
        st.table(pd.DataFrame(st.session_state.data['journal']).tail(5))
    else: st.info("لا توجد حركات مسجلة")

# --- 2. المستودعات ---
elif menu == "📦 المستودعات":
    st.header("📦 إدارة المخزون والجرد")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 الجرد الحالي")
        st.write(st.session_state.data['inventory'])
    with col2:
        st.subheader("📥 إضافة بضاعة")
        item = st.selectbox("المادة", ["مواد خام", "منتج جاهز"])
        qty = st.number_input("الكمية", min_value=1)
        if st.button("تحديث المخزن 🟠"):
            st.session_state.data['inventory'][item] += qty
            st.success("تم تحديث المستودع")

# --- 3. خط التصنيع ---
elif menu == "🏭 خط التصنيع":
    st.header("🏭 قسم الإنتاج والتصنيع")
    st.info("هنا يتم تحويل المواد الخام إلى منتجات جاهزة (خصم من مخزن الخام وإضافة للجاهز)")
    with st.form("prod_form"):
        raw_qty = st.number_input("كمية الخام المستخدمة", min_value=1)
        res_qty = st.number_input("كمية المنتج الجاهز الناتجة", min_value=1)
        if st.form_submit_button("بدء عملية التصنيع ⚙️"):
            if st.session_state.data['inventory']['مواد خام'] >= raw_qty:
                st.session_state.data['inventory']['مواد خام'] -= raw_qty
                st.session_state.data['inventory']['منتج جاهز'] += res_qty
                st.success("تمت عملية التصنيع بنجاح وترحيلها للمخازن")
            else: st.error("المواد الخام غير كافية!")

# --- 4. المشتريات (الموردين) ---
elif menu == "🧾 المشتريات (الموردين)":
    st.header("🤝 إدارة الموردين والمشتريات")
    with st.form("pur_form"):
        sup = st.selectbox("اختر المورد", st.session_state.data['suppliers'])
        val = st.number_input("قيمة الفاتورة", min_value=0.0)
        if st.form_submit_button("حفظ فاتورة الشراء"):
            st.session_state.data['journal'].append({'التاريخ': '2026-03-24', 'البيان': f'شراء من {sup}', 'مدين': 0, 'دائن': val})
            st.success("تم تسجيل الفاتورة في حساب المورد")

# --- 5. المبيعات (العملاء) ---
elif menu == "💰 المبيعات (العملاء)":
    st.header("🛒 فاتورة بيع للعملاء")
    with st.form("sale_form"):
        cus = st.selectbox("اسم العميل", st.session_state.data['customers'])
        val = st.number_input("مبلغ البيع", min_value=0.0)
        if st.form_submit_button("إصدار فاتورة بيع 🟠"):
            st.session_state.data['journal'].append({'التاريخ': '2026-03-24', 'البيان': f'بيع لـ {cus}', 'مدين': val, 'دائن': 0})
            st.success("تم إصدار الفاتورة وقبض المبلغ في الصندوق")

# --- 6. الموظفين ---
elif menu == "👥 الموظفين":
    st.header("👥 كادر العمل والرواتب")
    for emp in st.session_state.data['employees']:
        st.write(f"👤 {emp} - [صرف راتب] - [كشف دوام]")
    new_emp = st.text_input("إضافة موظف جديد")
    if st.button("إضافة 👤"):
        st.session_state.data['employees'].append(new_emp)
        st.rerun()

# --- 7. الحسابات الختامية ---
elif menu == "⚖️ الحسابات الختامية":
    st.header("⚖️ ميزان المراجعة والأرباح والخسائر")
    if st.session_state.data['journal']:
        df = pd.DataFrame(st.session_state.data['journal'])
        st.dataframe(df, use_container_width=True)
        st.metric("صافي الدخل", f"{df['مدين'].sum() - df['دائن'].sum()} $")
    else: st.warning("لا توجد حركات مالية بعد.")
