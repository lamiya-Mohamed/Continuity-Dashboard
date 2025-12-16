import streamlit as st
import os
import pandas as pd  # لاستخدام DataFrame مع st.bar_chart

# ========================
# تعريف كلاس المجال
# ========================
class ContinuityArea:
    def __init__(self, name, readiness_score, description):
        self.name = name
        self.readiness_score = readiness_score
        self.description = description

    def display_info(self):
        return f"المجال: {self.name} | درجة الجاهزية: {self.readiness_score} | الوصف: {self.description}"

    def update_score(self, new_score):
        self.readiness_score = new_score

# ========================
# تعريف كلاس Dashboard
# ========================
class Dashboard:
    def __init__(self):
        if "areas_list" not in st.session_state:
            st.session_state.areas_list = []

    def add_area(self, area):
        st.session_state.areas_list.append(area)

    def display_all_areas(self):
        return [area.display_info() for area in st.session_state.areas_list]

    def plot_readiness(self):
        if not st.session_state.areas_list:
            st.warning("لا يوجد بيانات للرسم.")
            return
        # تحويل البيانات لـ DataFrame
        df = pd.DataFrame({
            "المجالات": [area.name for area in st.session_state.areas_list],
            "درجة الجاهزية": [area.readiness_score for area in st.session_state.areas_list]
        })
        st.bar_chart(data=df.set_index("المجالات"))

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            for area in st.session_state.areas_list:
                file.write(f"{area.name},{area.readiness_score},{area.description}\n")
        st.success("تم حفظ البيانات في الملف بنجاح.")

    def load_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                st.session_state.areas_list = []
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == 3:
                        name = data[0]
                        readiness_score = int(data[1])
                        description = data[2]
                        area = ContinuityArea(name, readiness_score, description)
                        st.session_state.areas_list.append(area)
            st.success("تم تحميل البيانات من الملف بنجاح.")
        except FileNotFoundError:
            st.error("الملف غير موجود.")

# ========================
# البرنامج الرئيسي Streamlit
# ========================
st.title("لوحة متابعة جاهزية المجالات")
dash = Dashboard()

# --- إضافة مجال جديد ---
st.header("إضافة مجال جديد")
with st.form("add_area_form"):
    name = st.text_input("اسم المجال")
    readiness = st.number_input("درجة الجاهزية (0-100)", min_value=0, max_value=100)
    description = st.text_area("الوصف")
    submitted = st.form_submit_button("إضافة المجال")
    if submitted:
        area = ContinuityArea(name, readiness, description)
        dash.add_area(area)
        st.success("تم إضافة المجال بنجاح.")

# --- عرض جميع المجالات ---
st.header("عرض جميع المجالات")
areas_info = dash.display_all_areas()
if areas_info:
    for info in areas_info:
        st.write(info)
else:
    st.info("لا يوجد مجالات حالياً.")

# --- تعديل درجة الجاهزية ---
st.header("تعديل درجة الجاهزية لمجال")
with st.form("update_score_form"):
    update_name = st.text_input("أدخل اسم المجال لتعديل الجاهزية", key="update_name")
    new_score = st.number_input("أدخل درجة الجاهزية الجديدة (0-100)", min_value=0, max_value=100, key="new_score")
    update_submitted = st.form_submit_button("تحديث الجاهزية")
    if update_submitted:
        found = False
        for area in st.session_state.areas_list:
            if area.name == update_name:
                area.update_score(new_score)
                found = True
                st.success("تم تحديث درجة الجاهزية.")
                break
        if not found:
            st.error("المجال غير موجود.")

# --- رسم Bar Chart ---
st.header("رسم Bar Chart لكل المجالات")
if st.button("عرض الرسم البياني"):
    dash.plot_readiness()

# --- حفظ البيانات ---
st.header("حفظ البيانات في ملف")
save_filename = st.text_input("أدخل اسم الملف لحفظ البيانات", key="save_file")
if st.button("حفظ الملف"):
    if save_filename:
        dash.save_to_file(save_filename)
    else:
        st.warning("من فضلك أدخل اسم الملف.")

# --- قراءة البيانات ---
st.header("قراءة البيانات من ملف")
load_filename = st.text_input("أدخل اسم الملف لقراءة البيانات", key="load_file")
if st.button("تحميل الملف"):
    if load_filename:
        dash.load_from_file(load_filename)
    else:
        st.warning("من فضلك أدخل اسم الملف.")

# --- حذف الملف ---
st.header("حذف ملف")
delete_filename = st.text_input("أدخل اسم الملف للحذف", key="delete_file")
if st.button("حذف الملف"):
    if delete_filename:
        if os.path.exists(delete_filename):
            os.remove(delete_filename)
            st.success("تم حذف الملف.")
        else:
            st.error("الملف غير موجود.")
