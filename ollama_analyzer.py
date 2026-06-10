import requests

def analyze_metrics(cpu, ram, disk):

    prompt = f"""
    You are an AI DevOps Engineer.

    Analyze these server metrics:

    CPU Usage: {cpu}%
    RAM Usage: {ram}%
    Disk Usage: {disk}%

    Provide:
    1. Incident Summary
    2. Possible Root Cause
    3. Severity
    4. Recommended Actions

    Keep the response professional.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]