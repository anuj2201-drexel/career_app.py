import streamlit as st
from spellchecker import SpellChecker
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Career Suggestion App", layout="wide")
st.title("🔍 Career Suggestion App for Students (with Smart Summary)")

# Load Career Cluster and Role Mapping
data_file = "career_clusters.json"
if not os.path.exists(data_file):
    st.error("Missing career_clusters.json file. Please upload it.")
    st.stop()

with open(data_file, "r", encoding="utf-8") as f:
    career_data = json.load(f)

career_domains = list(career_data.keys())
domain_keywords = [" ".join(career_data[cluster]["keywords"]) for cluster in career_domains]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(domain_keywords)

st.markdown("---")
st.markdown("### 🧠 Tell us more about you")

# Input fields
student_inputs = {
    "interests": st.text_area("1️⃣ What are your interests or hobbies?"),
    "dislikes": st.text_area("2️⃣ What subjects or activities do you NOT like?"),
    "strengths": st.text_area("3️⃣ What do you think you're good at (skills, subjects, etc.)?"),
    "achievements": st.text_area("4️⃣ Share any achievements or proud moments (optional):"),
    "confusions": st.text_area("5️⃣ Are you confused about anything? Tell us (optional):")
}

# Spell correction and abbreviation handling
spell = SpellChecker()
term_expansions = {
    "bio": "biology",
    "eco": "economics",
    "comp": "computer science",
    "maths": "mathematics",
    "gymn": "gym",
    "cs": "computer science",
    "acc": "accounting",
    "hist": "history",
    "geo": "geography",
    "sci": "science",
    "biz": "business",
    "eng": "english"
}

def clean_and_expand_text(text):
    if not text.strip():
        return ""
    words = text.lower().split()
    corrected = []
    for word in words:
        if word in term_expansions:
            corrected.append(term_expansions[word])
        else:
            corrected_word = spell.correction(word)
            corrected.append(corrected_word if corrected_word else word)
    return " ".join(corrected)

if st.button("🔎 Analyze My Career Fit"):
    with st.spinner("Analyzing your responses and preparing your career summary..."):

        # Combine and correct all student text
        corrected_inputs = {k: clean_and_expand_text(v) for k, v in student_inputs.items() if v.strip() != ""}
        combined_corrected = " ".join(corrected_inputs.values())

        # Smart Summary
        summary_parts = []
        if corrected_inputs.get("interests"):
            summary_parts.append(f"You're interested in {corrected_inputs['interests']}.")
        if corrected_inputs.get("dislikes"):
            summary_parts.append(f"You dislike {corrected_inputs['dislikes']}.")
        if corrected_inputs.get("strengths"):
            summary_parts.append(f"Your strengths include {corrected_inputs['strengths']}.")
        if corrected_inputs.get("achievements"):
            summary_parts.append(f"You've achieved things like {corrected_inputs['achievements']}.")
        if corrected_inputs.get("confusions"):
            summary_parts.append(f"You're currently confused about {corrected_inputs['confusions']}.")

        final_summary = " ".join(summary_parts).capitalize()

        # NLP match
        query_vec = vectorizer.transform([combined_corrected])
        similarity = cosine_similarity(query_vec, X)[0]

        ranked_indices = similarity.argsort()[::-1]
        top_matches = [(career_domains[i], similarity[i]) for i in ranked_indices if similarity[i] > 0.2]
        unsuitable_matches = [(career_domains[i], similarity[i]) for i in ranked_indices if similarity[i] < 0.05]

        st.subheader("📝 Your Profile Summary:")
        st.info(final_summary if final_summary else "We couldn’t summarize due to missing input.")

        st.markdown("---")
        st.subheader("🎯 Career Suggestions")

        if top_matches:
            st.success("✅ **Most Suitable Career Clusters:**")
            for cluster, score in top_matches:
                st.write(f"- {cluster} ({round(score * 100, 1)}%)")
                st.markdown(f"Top Roles: {', '.join(career_data[cluster]['careers'][:3])}")
        else:
            st.warning("No strong matches found. Try entering more detailed responses.")

        if unsuitable_matches:
            st.error("🚫 **Less Suitable Domains (based on your dislikes or weaknesses):**")
            for domain, score in unsuitable_matches[:3]:
                st.write(f"- {domain}")

        st.markdown("---")
        st.subheader("💬 Ask a follow-up question")
        chat_q = st.text_input("Want to know more about one of the careers suggested?")
        if chat_q:
            st.info("This version is offline. Detailed answers will be part of next update with AI support.")

        st.markdown("---")
        if st.button("🔁 Start Over"):
            st.experimental_rerun()
