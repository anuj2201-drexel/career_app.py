
import streamlit as st
from deep_translator import GoogleTranslator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Load pre-written FAQ if needed
with open("career_faq.json", "r", encoding="utf-8") as f:
    career_faq = json.load(f)

st.set_page_config(page_title="Career Discovery App", layout="wide")
st.title("🎓 Career Discovery Companion")
st.markdown("This AI-driven tool helps you find the best career options based on your interests, hobbies, and achievements.")

# Language support
languages = {
    "English": "en", "Hindi": "hi", "Marathi": "mr", "Gujarati": "gu",
    "Tamil": "ta", "Telugu": "te", "Kannada": "kn", "Bengali": "bn",
    "Punjabi": "pa", "Malayalam": "ml"
}
selected_language = st.selectbox("Select your language", list(languages.keys()))
lang_code = languages[selected_language]

def translate_text(text, target_lang):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except:
        return text

# Career domains
career_domains = [
    "Medicine & Healthcare", "Engineering & Technology", "Installation, Maintenance & Repair",
    "Information Technology", "Environmental & Biological Science", "Physical Science",
    "Transportation & Material Moving", "Business, Accounts & Finance", "Management", "Sales",
    "Arts, Design, Media & Communication", "Education, Training & Library", "Community & Social Service",
    "Social Science", "Office Support & Administration", "Personal Care & Service",
    "Law Enforcement & Protective Service"
]

# NLP Keyword dictionary per domain
domain_keywords = {
    "Information Technology": ["coding", "programming", "software", "developer", "AI", "data", "computers"],
    "Medicine & Healthcare": ["doctor", "nurse", "medicine", "surgery", "hospital", "patient", "health"],
    "Engineering & Technology": ["machines", "engineering", "mechanical", "civil", "electrical", "robotics"],
    "Business, Accounts & Finance": ["money", "finance", "bank", "investment", "CA", "accountant", "stocks"],
    "Arts, Design, Media & Communication": ["drawing", "painting", "acting", "writing", "media", "film", "design"],
    "Education, Training & Library": ["teaching", "training", "education", "library", "students", "coach"],
    "Social Science": ["psychology", "history", "geography", "politics", "economics"],
    "Law Enforcement & Protective Service": ["police", "law", "army", "defence", "security"],
    "Personal Care & Service": ["beautician", "hair", "salon", "spa", "styling", "cooking"],
}

# Collect inputs
inputs = {}
inputs["career_like"] = st.text_area(translate_text("Which careers do you like?", lang_code))
inputs["career_dislike"] = st.text_area(translate_text("Which careers do you dislike?", lang_code))
inputs["subjects_like"] = st.text_area(translate_text("Which subjects do you enjoy in school?", lang_code))
inputs["subjects_dislike"] = st.text_area(translate_text("Which subjects do you dislike?", lang_code))
inputs["hobbies"] = st.text_area(translate_text("List your hobbies and any personal achievements", lang_code))

# Combine input text
combined_text = " ".join(inputs.values()).lower()

# Intelligent keyword match
def match_domains(text):
    scores = {domain: 0 for domain in career_domains}
    for domain, keywords in domain_keywords.items():
        for word in keywords:
            if word in text:
                scores[domain] += 1
    return scores

# Interactive fallback questions
def ask_additional_questions():
    st.subheader("📋 Help us know more about you")
    q1 = st.radio("Do you prefer working alone or in teams?", ["Alone", "Teams", "Both"])
    q2 = st.radio("Do you enjoy physical, creative or analytical work?", ["Physical", "Creative", "Analytical"])
    q3 = st.radio("Would you like to help people directly in your job?", ["Yes", "No", "Not sure"])
    return f"{q1} {q2} {q3}"

# Show result after submit
if st.button("Submit"):
    if len(combined_text.strip()) < 15:
        st.warning("Your answers were not detailed enough. Answer some more questions below:")
        more_text = ask_additional_questions()
        combined_text += " " + more_text.lower()

    matched_scores = match_domains(combined_text)
    sorted_domains = sorted(matched_scores.items(), key=lambda x: x[1], reverse=True)
    suitable = [domain for domain, score in sorted_domains if score > 0]
    unsuitable = [domain for domain, score in sorted_domains if score == 0]

    if suitable:
        st.success("✅ Suitable Career Domains:")
        for domain in suitable:
            st.write(f"- {domain}")
    else:
        st.warning("⚠️ No strong career domains detected. Please try giving more specific examples.")

    if unsuitable:
        st.info("🚫 Unsuitable Career Domains:")
        for domain in unsuitable[:5]:
            st.write(f"- {domain}")

    st.subheader("🎯 Ask follow-up questions about these careers:")
    user_q = st.text_input("Type your career question (e.g., 'What does an IT engineer do?')")
    if user_q:
        found = False
        for cat, qa in career_faq.items():
            for pair in qa:
                if any(keyword in user_q.lower() for keyword in pair["q"].lower().split()):
                    st.write(f"💬 **{pair['a']}**")
                    found = True
                    break
        if not found:
            st.info("Sorry, I don't have an answer for that yet. Please ask another question.")

    if st.button("🔁 Restart"):
        st.experimental_rerun()
