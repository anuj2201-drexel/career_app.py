import streamlit as st
from textblob import TextBlob
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Career Suggestion App", layout="wide")
st.title("🔍 Career Suggestion App for Students (with Smart Summary)")

# Load FAQ or career mapping data
if not os.path.exists("career_faq.json"):
    st.error("Missing career_faq.json file. Please upload it.")
    st.stop()

with open("career_faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# Extract career domains and sample keywords
career_domains = list(faq_data.keys())
domain_keywords = [" ".join(faq_data[domain]) for domain in career_domains]

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

def correct_text(text):
    try:
        return str(TextBlob(text).correct())
    except Exception:
        return text

if st.button("🔎 Analyze My Career Fit"):
    with st.spinner("Analyzing your responses and preparing your career summary..."):

        # Combine and correct all student text
        combined_inputs = " ".join(student_inputs.values())

        corrected_inputs = {k: correct_text(v) for k, v in student_inputs.items() if v.strip() != ""}
        combined_corrected = " ".join(corrected_inputs.values())

        # Summary construction
        summary_parts = []
        if corrected_inputs.get("interests"):
            summary_parts.append(f"You mentioned being interested in {corrected_inputs['interests'].lower()}.")
        if corrected_inputs.get("dislikes"):
            summary_parts.append(f"You don’t enjoy {corrected_inputs['dislikes'].lower()}.")
        if corrected_inputs.get("strengths"):
            summary_parts.append(f"You believe your strengths are {corrected_inputs['strengths'].lower()}.")
        if corrected_inputs.get("achievements"):
            summary_parts.append(f"You’re proud of accomplishments like {corrected_inputs['achievements'].lower()}.")
        if corrected_inputs.get("confusions"):
            summary_parts.append(f"You’re confused about {corrected_inputs['confusions'].lower()}.")

        final_summary = " ".join(summary_parts)

        # NLP match
        query_vec = vectorizer.transform([combined_corrected])
        similarity = cosine_similarity(query_vec, X)[0]

        ranked_indices = similarity.argsort()[::-1]
        top_matches = [(career_domains[i], similarity[i]) for i in ranked_indices if similarity[i] > 0.2 and career_domains[i].lower() not in ["people", "things"]]

        unsuitable_matches = [(career_domains[i], similarity[i]) for i in ranked_indices if similarity[i] < 0.05]

        st.subheader("📝 Your Profile Summary:")
        st.info(final_summary if final_summary else "We couldn’t summarize due to missing input.")

        st.markdown("---")
        st.subheader("🎯 Career Suggestions")

        if top_matches:
            st.success("✅ **Suitable Career Domains:**")
            for domain, score in top_matches:
                st.write(f"- {domain} ({round(score*100, 1)}%)")
        else:
            st.warning("No strong matches found. Try entering more detailed responses.")

        if unsuitable_matches:
            st.error("🚫 **Less Suitable Domains (based on your dislikes or weaknesses):**")
            for domain, score in unsuitable_matches[:3]:
                st.write(f"- {domain}")

        # Chat-style question box
        st.markdown("---")
        st.subheader("💬 Ask a follow-up question")
        chat_q = st.text_input("Want to know more about one of the careers suggested?")
        if chat_q:
            st.info("This version is offline. Detailed answers will be part of next update with AI support.")

        # Reset option
        st.markdown("---")
        if st.button("🔁 Start Over"):
            st.experimental_rerun()
