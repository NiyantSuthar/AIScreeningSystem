from google import genai
import json


# Put your NEW API key here
client = genai.Client(api_key="Enter_Your_API_Key_Here")

def analyze_resume(resume_text, role, job_description):

    prompt = f"""
You are an expert HR AI assistant.

Return response ONLY in valid JSON format like this:

{{
  "name": "Candidate Name",
  "skills": "comma separated skills",
  "experience_years": "number or null",
  "score": number (out of 10),
  "feedback": "short feedback"
}}

Job Role: {role}
Job Description: {job_description}

Resume:
{resume_text[:6000]}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text