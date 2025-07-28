import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# Sample data for career domains
career_domains = {
    "Arts": ["drawing", "painting", "storytelling", "graphic novels", "design", "music"],
    "Healthcare": ["helping people", "hospital", "nursing", "medicine", "care"],
    "STEM": ["science", "technology", "math", "engineering", "coding", "experiments"],
    "Social Work": ["volunteering", "helping", "community", "ngo", "stray animals"],
    "Business": ["entrepreneur", "sales", "marketing", "management", "money"],
    "Education": ["teaching", "learning", "school", "tutoring"]
}

def get_relevant_domains(text):
    text = text.lower()
    domain_scores = {}
    for domain, keywords in career_domains.items():
        matches = sum([1 for kw in keywords if kw in text])
        domain_scores[domain] = matches
    sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
    relevant = [d for d, score in sorted_domains if score > 0]
    return relevant, sorted_domains

# App layout
st.set_page_config(page_title="Career Suggestion App", layout="centered")
st.title("🔍 Career Discovery App for Students")

# Language selection (simplified UI only)
language = st.selectbox("Select Language", ["English", "Hindi", "Marathi", "Tamil", "Telugu", "Gujarati", "Bengali", "Kannada", "Malayalam", "Punjabi"])

st.markdown("Please answer the following questions in simple sentences:")

interests = st.text_area("1. What are your interests?")
dislikes = st.text_area("2. What are your dislikes or things you don’t enjoy?")
achievements = st.text_area("3. What are your achievements?")
hobbies = st.text_area("4. What are your hobbies?")
confused_about = st.text_area("5. What are you confused about or unsure in choosing?")

if st.button("🔍 Find Career Suggestions"):
    full_text = f"{interests}\n{dislikes}\n{achievements}\n{hobbies}\n{confused_about}"
    relevant, domain_scores = get_relevant_domains(full_text)

    # Handle inconclusive data
    if not relevant:
        st.warning("We need a bit more information. Please answer these follow-up questions:")
        follow_up_1 = st.text_input("What school subjects do you enjoy or hate?")
        follow_up_2 = st.text_input("Have you ever imagined your future self doing something?")
        follow_up_3 = st.text_input("What makes you feel proud or excited?")

        full_text += f"\n{follow_up_1}\n{follow_up_2}\n{follow_up_3}"
        relevant, domain_scores = get_relevant_domains(full_text)

    # Paraphrased Summary
    if any([interests, dislikes, achievements, hobbies, confused_about]):
        summary = f"You mentioned that you're interested in {interests.strip().lower() or 'various topics'}, but not very fond of {dislikes.strip().lower() or 'certain things'}. You have achieved {achievements.strip().lower() or 'some notable things'}, and enjoy spending time on hobbies like {hobbies.strip().lower() or 'different activities'}. You're feeling unsure about {confused_about.strip().lower() or 'a clear path ahead'}."
        st.markdown("### 📌 Summary of What You Shared")
        st.info(summary)

    st.markdown("### ✅ Suggested Career Domains:")
    if relevant:
        for domain in relevant[:3]:
            st.success(f"- {domain}")
    else:
        st.error("Still not enough information to determine suitable careers. Please try again.")

    st.markdown("### 💬 Have questions about these careers?")
    query = st.text_input("Type your question here:")
    if query:
        st.markdown(f"(Simulated) You asked: **{query}**")
        st.markdown("This is where an intelligent response would appear. 🤖")
