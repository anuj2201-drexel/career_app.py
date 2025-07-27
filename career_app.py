import streamlit as st
from deep_translator import DeepL

# ------------------ Initial Setup ------------------ #
st.set_page_config(page_title="Career Counsellor AI", layout="wide")
st.title("🎓 Career Counsellor AI (India Specific)")

st.markdown("""
This tool analyses a student's career preferences, dislikes, subjects, and hobbies to recommend suitable career domains and job roles. Built for Indian students across streams (Science, Commerce, Humanities).
""")

# ------------------ Language Selection ------------------ #
languages = {
    "English": "EN",
    "Hindi": "HI",
    "Marathi": "MR",
    "Gujarati": "GU",
    "Bengali": "BN",
    "Tamil": "TA",
    "Telugu": "TE",
    "Kannada": "KN",
    "Malayalam": "ML",
    "Punjabi": "PA"
}

selected_lang = st.selectbox("Choose your language (अपनी भाषा चुनें)", list(languages.keys()))
language_code = languages[selected_lang]

# Helper to translate prompts
def t(text):
    try:
        return DeepL(source='EN', target=language_code).translate(text)
    except:
        return text

# ------------------ Input Form ------------------ #
if 'step' not in st.session_state:
    st.session_state.step = 0

if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

if 'final_go' not in st.session_state:
    st.session_state.final_go = []

if 'final_no_go' not in st.session_state:
    st.session_state.final_no_go = []

if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []

if 'follow_ups' not in st.session_state:
    st.session_state.follow_ups = {}

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

def ask_follow_up():
    st.session_state.follow_ups['q4'] = st.selectbox(t("4️⃣ Which of these activities do you enjoy most?"), [
        t("Helping people"),
        t("Fixing or building things"),
        t("Solving puzzles or logical problems"),
        t("Being on stage or drawing/creating"),
        t("Learning about business or money")
    ])
    st.session_state.follow_ups['q5'] = st.selectbox(t("5️⃣ What is your favorite school project type?"), [
        t("Group work"), t("Solo research"), t("Art and design"), t("Presentation or speech"), t("Experiment or model")
    ])
    st.session_state.follow_ups['q6'] = st.selectbox(t("6️⃣ If you had to pick a club, which one would it be?"), [
        t("Science Club"), t("Drama Club"), t("Coding Club"), t("Environment Club"), t("Debate Club")
    ])

if st.session_state.step == 0:
    with st.form("basic_form"):
        st.header(t("📝 Enter Student Information"))
        st.session_state.user_data['career_like'] = st.text_area(t("Careers you like"), help=t("Eg. Doctor, Engineer, IAS, Designer"))
        st.session_state.user_data['career_dislike'] = st.text_area(t("Careers you dislike"))
        st.session_state.user_data['subject_like'] = st.text_area(t("Subjects you like"), help=t("Eg. Biology, History, Computer Science"))
        st.session_state.user_data['subject_dislike'] = st.text_area(t("Subjects you dislike"))
        st.session_state.user_data['hobbies'] = st.text_area(t("Hobbies and Achievements"), help=t("Eg. Drawing, Coding, Football, NCC, Reading"))
        next_step = st.form_submit_button(t("Next"))
        if next_step:
            st.session_state.step = 1

elif st.session_state.step == 1:
    with st.form("extra_form"):
        st.header(t("🔍 Let's get to know your interests better"))
        st.session_state.user_data['q1'] = st.text_input(t("1️⃣ What kind of problems do you enjoy solving? (Eg. health, technology, environment, people)"))
        st.session_state.user_data['q2'] = st.text_input(t("2️⃣ Which kind of work would you prefer — indoor desk job, field job, creative or leadership roles?"))
        st.session_state.user_data['q3'] = st.text_input(t("3️⃣ Do you enjoy working with people, data, tools/machines, or ideas?"))

        submit_pre = st.form_submit_button(t("Next Step"))
        if submit_pre:
            all_likes_text = f"{st.session_state.user_data['career_like']} {st.session_state.user_data['subject_like']} {st.session_state.user_data['hobbies']} {st.session_state.user_data['q1']} {st.session_state.user_data['q2']} {st.session_state.user_data['q3']}".lower()
            go_domains = extract_domains(all_likes_text)
            if not go_domains:
                st.session_state.step = 1.5
            else:
                st.session_state.step = 2

elif st.session_state.step == 1.5:
    st.markdown("### " + t("We need a bit more help to guide you better."))
    with st.form("follow_up_form"):
        ask_follow_up()
        submit_all = st.form_submit_button(t("Show My Career Suggestions"))
        if submit_all:
            all_likes_text = f"{st.session_state.user_data['career_like']} {st.session_state.user_data['subject_like']} {st.session_state.user_data['hobbies']} {st.session_state.user_data['q1']} {st.session_state.user_data['q2']} {st.session_state.user_data['q3']} {st.session_state.follow_ups['q4']} {st.session_state.follow_ups['q5']} {st.session_state.follow_ups['q6']}".lower()
            all_dislikes_text = f"{st.session_state.user_data['career_dislike']} {st.session_state.user_data['subject_dislike']}".lower()

            go_domains = extract_domains(all_likes_text)
            no_go_domains = extract_domains(all_dislikes_text)

            st.session_state.final_go = [d for d in career_domains if d in go_domains and d not in no_go_domains]
            st.session_state.final_no_go = [d for d in career_domains if d in no_go_domains and d not in go_domains]

            st.session_state.suggestions = [k.title() for k, v in category_domain_map.items() if any(domain in st.session_state.final_go for domain in v)]

            st.session_state.step = 2

elif st.session_state.step == 2:
    st.subheader(t("📊 Career Analysis Result"))
    st.markdown("### ✅ " + t("Suitable Career Domains") + ":")
    st.write(st.session_state.final_go if st.session_state.final_go else t("Some more answers would help improve your result."))

    st.markdown("### 🚫 " + t("Unsuitable Career Domains") + ":")
    st.write(st.session_state.final_no_go if st.session_state.final_no_go else t("None detected."))

    st.markdown("### 🎯 " + t("Suggested Careers") + ":")
    st.write(st.session_state.suggestions[:10] if st.session_state.suggestions else t("More answers would help improve suggestions."))

    if st.button(t("🔁 Start Over")):
        st.session_state.step = 0
        st.session_state.user_data = {}
        st.session_state.final_go = []
        st.session_state.final_no_go = []
        st.session_state.suggestions = []
        st.session_state.follow_ups = {}
