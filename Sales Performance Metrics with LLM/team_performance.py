import pandas as pd
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_TOKEN = "YOUR_API_KEY"

# Function to calculate team-wide averages
def calculate_averages(data):
    return {
        "revenue": round(data['revenue_confirmed'].mean()),
        "leads": round(data['lead_taken'].mean()),
        "tours": round(data['tours_booked'].mean()),
        "applications": round(data['applications'].mean())
    }


# Function to summarize team performance using Hugging Face API
def summarize_performance(inputs):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
    }
    payload = {"inputs": inputs}

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to generate the team performance summary
def get_team_summary(data):
    averages = calculate_averages(data)

    summary_data = (
        f"Team-wide performance: Average revenue of ${averages['revenue']}, "
        f"{averages['leads']} leads taken, "
        f"{averages['tours']} tours booked, "
        f"{averages['applications']} applications processed."
    )

    result = summarize_performance(summary_data)
    summary_text = result[0]['summary_text'] if 'summary_text' in result[0] else "Error generating summary."

    return {"team_performance_summary": summary_text, "averages": averages}
