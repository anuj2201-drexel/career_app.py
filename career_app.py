import streamlit as st

# ------------------ Initial Setup ------------------ #
st.set_page_config(page_title="Career Counsellor AI", layout="wide")
st.title("🎓 Career Counsellor AI (India Specific)")

st.markdown("""
This tool analyses a student's career preferences, dislikes, subjects, and hobbies to recommend suitable career domains and job roles. Built for Indian students across streams (Science, Commerce, Humanities).
""")

# ------------------ Input Form ------------------ #
with st.form("career_form"):
    st.header("📝 Enter Student Information")
    career_like = st.text_area("Careers you like", help="Eg. Doctor, Engineer, IAS, Designer")
    career_dislike = st.text_area("Careers you dislike")
    subject_like = st.text_area("Subjects you like", help="Eg. Biology, History, Computer Science")
    subject_dislike = st.text_area("Subjects you dislike")
    hobbies = st.text_area("Hobbies and Achievements", help="Eg. Drawing, Coding, Football, NCC, Reading")
    submitted = st.form_submit_button("Analyze")

# ------------------ Core Logic ------------------ #
category_domain_map = {
    "doctor": ["Medicine & Healthcare"],
    "biology": ["Medicine & Healthcare", "Environmental & Biological Science"],
    "psychology": ["Community & Social Service", "Social Science"],
    "engineer": ["Engineering & Technology"],
    "coding": ["Information Technology"],
    "computer": ["Information Technology"],
    "law": ["Law Enforcement & Protective Service"],
    "teaching": ["Education, Training & Library"],
    "drawing": ["Arts, Design, Media & Communication"],
    "accounting": ["Business, Accounts & Finance"],
    "math": ["Engineering & Technology", "Information Technology"],
    "history": ["Social Science"],
    "football": ["Personal Care & Service"],
    "ias": ["Law Enforcement & Protective Service", "Management"],
    "design": ["Arts, Design, Media & Communication"],
    "commerce": ["Business, Accounts & Finance"],
    "physics": ["Physical Science"],
    "chemistry": ["Physical Science"],
    "environment": ["Environmental & Biological Science"],
    "media": ["Arts, Design, Media & Communication"]
}

career_domains = [
    "Medicine & Healthcare", "Engineering & Technology", "Installation, Maintenance & Repair",
    "Information Technology", "Environmental & Biological Science", "Physical Science",
    "Transportation & Material Moving", "Business, Accounts & Finance", "Management",
    "Sales", "Arts, Design, Media & Communication", "Education, Training & Library",
    "Community & Social Service", "Social Science", "Office Support & Administration",
    "Personal Care & Service", "Law Enforcement & Protective Service"
]

if submitted:
    st.subheader("📊 Career Analysis Result")

    # Combine and lowercase all inputs
    all_likes_text = f"{career_like} {subject_like} {hobbies}".lower()
    all_dislikes_text = f"{career_dislike} {subject_dislike}".lower()

    go_domains = set()
    no_go_domains = set()

    for keyword, domains in category_domain_map.items():
        if keyword in all_likes_text:
            go_domains.update(domains)
        if keyword in all_dislikes_text:
            no_go_domains.update(domains)

    final_go = [d for d in career_domains if d in go_domains and d not in no_go_domains]
    final_no_go = [d for d in career_domains if d in no_go_domains and d not in go_domains]

    st.markdown("### ✅ Suitable Career Domains:")
    st.write(final_go if final_go else "No clear domains identified from the inputs.")

    st.markdown("### 🚫 Unsuitable Career Domains:")
    st.write(final_no_go if final_no_go else "None detected.")

    # Suggest careers based on go domains
    st.markdown("### 🎯 Suggested Careers:")
    suggestions = [k.title() for k, v in category_domain_map.items() if any(domain in final_go for domain in v)]
    st.write(suggestions[:10] if suggestions else "Not enough data to suggest careers.")
