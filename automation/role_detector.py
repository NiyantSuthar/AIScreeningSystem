def detect_role(subject):

    subject = subject.lower()

    if any(word in subject for word in ["software", "developer", "engineer", "backend", "frontend", "tech"]):
        return "TECHNICAL"

    elif any(word in subject for word in ["hr", "recruiter"]):
        return "HR"

    elif any(word in subject for word in ["marketing", "sales", "operations"]):
        return "NON_TECHNICAL"

    else:
        return "UNKNOWN"