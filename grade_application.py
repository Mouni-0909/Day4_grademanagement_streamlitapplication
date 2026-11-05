
import streamlit as st
import pandas as pd
import os

# Page settings
st.set_page_config(page_title="SEAITrack", page_icon="🎓", layout="wide")

# Professional UI design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(rgba(244,247,251,0.92), rgba(244,247,251,0.92)),
    url("https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1600");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stSidebar"] {
    background-color: #172D4B;
}

[data-testid="stSidebar"] * {
    color: white;
}

h1, h2, h3 {
    color: #172D4B;
}

[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

.stButton button, .stDownloadButton button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)


# Load student records
if os.path.exists("students.csv"):
    students = pd.read_csv("students.csv")
else:
    students = pd.DataFrame(columns=["ID", "Name", "Class", "Mark", "Grade"])


# Grade calculation
def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


# Sidebar navigation
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.title("🎓 SEAITrack")

    st.title("Student Management")
    st.caption("Academic Performance Portal")
    st.markdown("---")

    menu = st.radio("Navigation",
        ["Dashboard", "Add Student", "View Students", "Delete Student"])


# Dashboard
if menu == "Dashboard":
    st.title("Welcome to SEAITrack 👋")
    st.write("Student Grade Management Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", len(students))

    if len(students) > 0:
        col2.metric("Average Marks", round(students["Mark"].mean(), 2))
        col3.metric("Highest Marks", students["Mark"].max())
        col4.metric("Lowest Marks", students["Mark"].min())
    else:
        col2.metric("Average Marks", 0)
        col3.metric("Highest Marks", 0)
        col4.metric("Lowest Marks", 0)

    st.markdown("---")
    st.subheader("Student Records")
    st.dataframe(students, use_container_width=True, hide_index=True)


# Add Student
elif menu == "Add Student":
    st.title("➕ Add New Student")
    st.write("Enter student details below.")

    with st.form("student_form"):
        student_id = st.text_input("Student ID")
        name = st.text_input("Student Name")
        student_class = st.text_input("Class")
        mark = st.number_input("Enter Marks", 0, 100, 0)
        submit = st.form_submit_button("Add Student")

    if submit:
        if not student_id.strip() or not name.strip() or not student_class.strip():
            st.error("Please enter all details.")

        elif student_id.strip().lower() in students["ID"].astype(str).str.lower().values:
            st.error("Student ID already exists.")

        else:
            grade = get_grade(mark)

            students.loc[len(students)] = [
                student_id.strip(), name.strip(),
                student_class.strip(), mark, grade
            ]

            students.to_csv("students.csv", index=False)
            st.success(f"Student {name} added successfully! Grade: {grade}")


# View Students
elif menu == "View Students":
    st.title("📋 Student Records")

    search = st.text_input("Search by Student Name or ID")

    result = students[
        students["Name"].str.contains(search, case=False, na=False)
        | students["ID"].astype(str).str.contains(search, case=False, na=False)
    ]

    st.dataframe(result, use_container_width=True, hide_index=True)

    st.download_button(
        "📥 Download Student Records",
        result.to_csv(index=False),
        "students.csv"
    )


# Delete Student
elif menu == "Delete Student":
    st.title("🗑️ Delete Student Record")

    if len(students) > 0:
        student_id = st.selectbox("Select Student ID", students["ID"])

        if st.button("Delete Student"):
            students = students[students["ID"].astype(str) != str(student_id)]
            students.to_csv("students.csv", index=False)
            st.success("Student deleted successfully!")
            st.rerun()
    else:
        st.info("No student records available.")


# Footer
st.markdown("---")
st.caption("© 2026 SEAITrack | Student Grade Management System")
