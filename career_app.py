import streamlit as st
import googletrans
from googletrans import Translator

# ------------------ Initial Setup ------------------ #
st.set_page_config(page_title="Career Counsellor AI", layout="wide")
st.title("🎓 Career Counsellor AI (India Specific)")

st.markdown("""
This tool analyses a student's career preferences, dislikes, subjects, and hobbies to recommend suitable career domains and job roles. Built for Indian students across streams (Science, Commerce, Humanities).
""")

# ------------------ Language Selection ------------------ #
languages = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa"
}

translator = Translator()
selected_lang = st.selectbox("Choose your language (अपनी भाषा चुनें)", list(languages.keys()))
language_code = languages[selected_lang]

# Helper to translate prompts

def t(text):
    try:
        return translator.translate(text, dest=language_code).text
    except:
        return text

# ------------------ Input Form ------------------ #
show_analysis = False
restart = False

if 'complete_input' not in st.session_state:
    st.session_state.complete_input = False

if 'final_go' not in st.session_state:
    st.session_state.final_go = []

if 'final_no_go' not in st.session_state:
    st.session_state.final_no_go = []

if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []

if not st.session_state.complete_input:
    with st.form("career_form"):
        st.header(t("📝 Enter Student Information"))
        career_like = st.text_area(t("Careers you like"), help=t("Eg. Doctor, Engineer, IAS, Designer"))
        career_dislike = st.text_area(t("Careers you dislike"))
        subject_like = st.text_area(t("Subjects you like"), help=t("Eg. Biology, History, Computer Science"))
        subject_dislike = st.text_area(t("Subjects you dislike"))
        hobbies = st.text_area(t("Hobbies and Achievements"), help=t("Eg. Drawing, Coding, Football, NCC, Reading"))
        submitted = st.form_submit_button(t("Analyze"))

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
        "media": ["Arts, Design, Media & Communication"],
        "training": ["Education, Training & Library"],
        "leadership": ["Management"],
        "people": ["Community & Social Service", "Sales"],
        "machines": ["Installation, Maintenance & Repair"],
        "data": ["Business, Accounts & Finance", "Information Technology"]
    }

    career_domains = [
        "Medicine & Healthcare", "Engineering & Technology", "Installation, Maintenance & Repair",
        "Information Technology", "Environmental & Biological Science", "Physical Science",
        "Transportation & Material Moving", "Business, Accounts & Finance", "Management",
        "Sales", "Arts, Design, Media & Communication", "Education, Training & Library",
        "Community & Social Service", "Social Science", "Office Support & Administration",
        "Personal Care & Service", "Law Enforcement & Protective Service"
    ]

    def extract_domains(text):
        domains = set()
        for keyword, domain_list in category_domain_map.items():
            if keyword in text:
                domains.update(domain_list)
        return domains

    def get_additional_data():
        with st.form("extra_form"):
            st.info(t("We need a bit more information to guide you better. Please answer the following:"))
            q1 = st.text_input(t("1️⃣ What kind of problems do you enjoy solving? (Eg. health, technology, environment, people)"))
            q2 = st.text_input(t("2️⃣ Which kind of work would you prefer — indoor desk job, field job, creative or leadership roles?"))
            q3 = st.text_input(t("3️⃣ Do you enjoy working with people, data, tools/machines, or ideas?"))
            confirm = st.form_submit_button(t("Submit Answers"))
            if confirm:
                return f"{q1} {q2} {q3}".lower()
        return None

    if submitted:
        all_likes_text = f"{career_like} {subject_like} {hobbies}".lower()
        all_dislikes_text = f"{career_dislike} {subject_dislike}".lower()

        go_domains = extract_domains(all_likes_text)
        no_go_domains = extract_domains(all_dislikes_text)

        final_go = [d for d in career_domains if d in go_domains and d not in no_go_domains]
        final_no_go = [d for d in career_domains if d in no_go_domains and d not in go_domains]

        attempt = 0
        while not final_go and attempt < 3:
            extra_input = get_additional_data()
            attempt += 1
            if extra_input:
                go_domains.update(extract_domains(extra_input))
                final_go = [d for d in career_domains if d in go_domains and d not in no_go_domains]
            else:
                break

        st.session_state.final_go = final_go
        st.session_state.final_no_go = final_no_go
        st.session_state.suggestions = [k.title() for k, v in category_domain_map.items() if any(domain in final_go for domain in v)]
        st.session_state.complete_input = True

if st.session_state.complete_input:
    st.subheader(t("📊 Career Analysis Result"))
    st.markdown("### ✅ " + t("Suitable Career Domains") + ":")
    st.write(st.session_state.final_go if st.session_state.final_go else t("No clear domains identified from the inputs."))

    st.markdown("### 🚫 " + t("Unsuitable Career Domains") + ":")
    st.write(st.session_state.final_no_go if st.session_state.final_no_go else t("None detected."))

    st.markdown("### 🎯 " + t("Suggested Careers") + ":")
    st.write(st.session_state.suggestions[:10] if st.session_state.suggestions else t("Not enough data to suggest careers."))

    if st.button(t("🔁 Start Over")):
        st.session_state.complete_input = False
        st.session_state.final_go = []
        st.session_state.final_no_go = []
        st.session_state.suggestions = []
