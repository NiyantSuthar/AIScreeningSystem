from automation.email_reader import fetch_unread_applications
from automation.role_detector import detect_role
from config.job_descriptions import TECH_JD, HR_JD, NON_TECH_JD
from automation.resume_parser import extract_text_from_pdf
from automation.ai_analyzer import analyze_resume
import json
import pandas as pd


def get_job_description(role):

    if role == "TECHNICAL":
        return TECH_JD
    elif role == "HR":
        return HR_JD
    elif role == "NON_TECHNICAL":
        return NON_TECH_JD
    else:
        return None


def main():

    print("🚀 Checking for new applications...")

    emails = fetch_unread_applications()
    all_results = []

    for email_data in emails:

        subject = email_data["subject"]
        role = detect_role(subject)
        print("Detected Role:", role)

        jd = get_job_description(role)

        if not jd:
            print("No Matching Job Description")
            continue

        if not email_data["attachment_path"]:
            continue

        resume_text = extract_text_from_pdf(
            email_data["attachment_path"]
        )

        if not resume_text:
            continue

        print("Sending to Gemini...")

        analysis_text = analyze_resume(
            resume_text,
            role,
            jd
        )

        print("AI RAW RESPONSE:")
        print(analysis_text)
        print("=" * 80)

        try:
            analysis_json = json.loads(analysis_text)

            all_results.append({
                "Name": analysis_json.get("name"),
                "Email": email_data["sender"],
                "Role": role,
                "Score": analysis_json.get("score"),
                "Experience": analysis_json.get("experience_years"),
                "Skills": analysis_json.get("skills"),
                "Feedback": analysis_json.get("feedback")
            })

        except json.JSONDecodeError:
            print("❌ JSON parsing failed for:", email_data["sender"])

    # After processing all resumes → Generate Ranked CSV
    if all_results:

        df = pd.DataFrame(all_results)

        df = df.sort_values(by="Score", ascending=False)

        df.to_csv("ranked_results.csv", index=False)

        print("✅ Ranked CSV generated: ranked_results.csv")

    else:
        print("No valid results to save.")


if __name__ == "__main__":
    main()