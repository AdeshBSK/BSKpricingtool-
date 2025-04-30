import streamlit as st
import pandas as pd
from PIL import Image
from pricing_logic import calculate_program_cost

st.set_page_config(page_title="BeyondSkool Pricing Wizard", layout="centered")

# CSS
st.markdown("""<style> ... </style>""", unsafe_allow_html=True)

# Branding
logo = Image.open("bsklogo.png")
st.image(logo, use_container_width=True)
st.title("BeyondSkool Pricing Wizard")

school_name = st.text_input("Name of the School")
programs_selected = st.multiselect("Select Program(s):", ["Communication", "Financial Literacy", "STEM"])
school_days = st.radio("School operates:", ["5 days a week", "6 days a week"], horizontal=True)
max_sections_per_teacher = 27 if school_days == "5 days a week" else 32

student_info = {}
if programs_selected:
    for prog in programs_selected:
        st.subheader(f"{prog} Program")
        students = st.number_input(f"Number of Students - {prog}", min_value=1, max_value=3000, step=1, key=f"students_{prog}")
        section_size = st.number_input(f"Students per Section - {prog}", min_value=10, max_value=60, step=5, value=30, key=f"section_{prog}")
        student_info[prog] = {"students": students, "section_size": section_size}

    if st.button("Calculate Pricing"):
        st.session_state.update({
            "school_name": school_name,
            "programs_selected": programs_selected,
            "student_info": student_info,
            "school_days": school_days,
            "calculate": True
        })

if st.session_state.get("calculate"):
    discount_percent = st.slider("Discount %", 0, 40, 0)
    st.markdown(f"<div class='discount-tab'><b>Discount:</b> {discount_percent}%</div>", unsafe_allow_html=True)

    total_price = 0
    total_cost = 0
    total_students = 0
    all_margins = []
    breakdown_rows = []

    st.subheader(f"Pricing Summary for {school_name}")

    for prog in programs_selected:
        data = student_info[prog]
        result, margin = calculate_program_cost(
            prog, data["students"], data["section_size"], max_sections_per_teacher, discount_percent, school_days
        )

        if result is None:
            st.error(f"No Pricing Available for {prog} – Margin Below 30%")
            continue

        all_margins.append(margin)
        total_price += result["final_price"]
        total_cost += result["final_price"] / ((100 - margin) / 100)
        total_students += result["students"]

        st.markdown(f"<div class='summary-box'><h3>{prog} Program</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='program-price'>Price per Student: ₹{round(result['price_per_student'])}</div>", unsafe_allow_html=True)
        st.markdown("<div class='teacher-icons'>", unsafe_allow_html=True)
        st.markdown(f"<span>👨‍🏫 Full-time Teachers: <b>{result['full_teachers']}</b></span>", unsafe_allow_html=True)
        if result["teacher_days"] > 0:
            st.markdown(f"<span>📅 Variable Teacher Days: <b>{result['teacher_days']} days/week</b></span>", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        breakdown_rows.append({
            "Program": prog,
            "Price per Student (₹)": round(result["price_per_student"]),
            "Book Cost (₹)": round(result["book"]),
            "Service Fee (₹)": round(result["service"]),
            "GST @18% (₹)": result["gst"],
            "Full-Time Teachers": result["full_teachers"],
            "Variable Days": result["teacher_days"]
        })

    if total_price > 0:
        avg_price = total_price / total_students
        avg_margin = sum(all_margins) / len(all_margins)

        st.markdown(f"<div class='big-price'>Total Price: ₹{round(total_price):,}</div>", unsafe_allow_html=True)
        st.markdown(f"**Average Price per Student:** ₹{round(avg_price):,}")
        st.markdown(f"**Total Students:** {total_students}")
        st.markdown(f"<div class='gross-margin-tab'>Gross Margin: {round(avg_margin)}%</div>", unsafe_allow_html=True)

        df = pd.DataFrame(breakdown_rows)
        st.markdown("### Breakdown Table")
        st.dataframe(df, use_container_width=True)

    if st.button("Go Back"):
        st.session_state["calculate"] = False
