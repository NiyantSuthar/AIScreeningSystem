import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.gemini_parser import analyze_resume

st.set_page_config(page_title="AI HR Screening System", layout="wide")

st.title("🤖 AI HR Resume Screening System")
st.markdown("### Smart AI-Based Resume Ranking")

st.markdown("---")

job_description = st.text_area("📄 Enter Job Description", height=200)

uploaded_files = st.file_uploader(
    "📂 Upload Candidate Resumes (PDF only)",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("🚀 Analyze Candidates"):

    if not uploaded_files:
        st.warning("Please upload at least one resume.")
        st.stop()

    if not job_description:
        st.warning("Please enter a job description.")
        st.stop()

    st.info("Analyzing resumes... Please wait.")

    candidates = []

    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        parsed_data = analyze_resume(text, job_description)

        candidates.append({
            "filename": file.name,
            "data": parsed_data
        })

    ranked_candidates = sorted(
        candidates,
        key=lambda x: x["data"].get("overall_score", 0),
        reverse=True
    )

    st.success(f"✅ {len(ranked_candidates)} Candidates Ranked Successfully")

    st.markdown("---")
    st.header("🏆 Final Ranking")

    for idx, candidate in enumerate(ranked_candidates, start=1):

        data = candidate["data"]
        score = data.get("overall_score", 0)

        # Medal Logic
        if idx == 1:
            badge = "🥇 TOP CANDIDATE"
        elif idx == 2:
            badge = "🥈 Strong Match"
        elif idx == 3:
            badge = "🥉 Potential Match"
        else:
            badge = f"Rank #{idx}"

        with st.expander(f"{badge} — {candidate['filename']} (Score: {score})", expanded=(idx <= 3)):

            col1, col2 = st.columns([1, 2])

            with col1:
                st.metric("Overall Score", score)
                st.progress(score / 100)

                st.metric("Skills Match", data.get("skills_match_score", 0))
                st.metric("Experience Match", data.get("experience_match_score", 0))

            with col2:
                st.markdown("### 🧾 AI Summary")
                st.write(data.get("summary", "No summary available."))

                st.markdown("### ✅ Matched Skills")
                matched = data.get("matched_skills", [])
                st.write(", ".join(matched) if matched else "None")

                st.markdown("### ❌ Missing Skills")
                missing = data.get("missing_skills", [])
                st.write(", ".join(missing) if missing else "None")

    st.markdown("---")
    st.info("Ranking complete. You can upload new resumes to re-evaluate.")