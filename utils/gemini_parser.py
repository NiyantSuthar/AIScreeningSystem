from google import genai
import os
import json

# Initialize client once
client = genai.Client(
    api_key="Enter your API key here",
    http_options={"api_version": "v1"}
)

def analyze_resume(resume_text, job_description):

    prompt = f"""
    You are an AI HR assistant.

    Job Description:
    {job_description}

    Resume:
    {resume_text}

    Return ONLY valid JSON:

    {{
        "candidate_name": "",
        "skills_match_score": 0,
        "experience_match_score": 0,
        "overall_score": 0,
        "matched_skills": [],
        "missing_skills": [],
        "summary": ""
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw_text = response.text.strip()

    # Remove markdown code block if present
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1].strip()
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {"error": raw_text}