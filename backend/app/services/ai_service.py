import ollama

def generate_summary(text: str):

    prompt = f"""
    You are a healthcare assistant.

    Summarize the clinical notes.

    Clinical Notes:
    {text}

    Return:
    1. Summary
    2. Recommendations
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "summary":
            response["message"]["content"],
        "recommendations":
            "Review manually",
        "confidence":
            0.95
    }


def patient_summary(patient: str, conditions: str, medications: str, observations: str):
    prompt = f"""
        Patient:
        {patient}

        Conditions:
        {conditions}

        Medications:
        {medications}

        Observations:
        {observations}

        Create:

        1. Clinical Summary
        2. Risk Assessment
        3. Recommendations
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "summary":
            response["message"]["content"],
        "recommendations":
            "Review manually",
        "confidence":
            0.95
    }