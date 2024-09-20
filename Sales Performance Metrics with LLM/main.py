from flask import Flask, request, jsonify, render_template
import requests
import pandas as pd
from team_performance import get_team_summary
from performance_trends import analyze_performance_trends

# Initialize Flask app
app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_TOKEN = "YOUR_API_KEY"  # Replace with your Hugging Face API token


data = pd.read_csv(r'C:\Users\ranam\Downloads\sales_performance_data.csv')


def summarize_performance(inputs):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
    }
    payload = {"inputs": inputs}

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


# Function to calculate team-wide averages
def calculate_averages(data):
    return {
        "revenue": round(data['revenue_confirmed'].mean()),
        "leads": round(data['lead_taken'].mean()),
        "tours": round(data['tours_booked'].mean()),
        "applications": round(data['applications'].mean())
    }


def evaluate_individual(employee_data, averages):
    name = employee_data['employee_name'].values[0]
    revenue = employee_data['revenue_confirmed'].values[0]
    leads = employee_data['lead_taken'].values[0]
    tours = employee_data['tours_booked'].values[0]
    applications = employee_data['applications'].values[0]

    performance_data_str = (
        f"Sales performance for {name}: "
        f"revenue of ${revenue}, "
        f"took {leads} leads, "
        f"booked {tours} tours, "
        f"processed {applications} applications."
    )

    result = summarize_performance(performance_data_str)
    summary_text = result[0]['summary_text'] if 'summary_text' in result[0] else "Error generating summary."

    # Simple performance evaluation logic
    performance_evaluation = evaluate_performance(revenue, leads, tours, applications, averages)

    return {"performance_summary": summary_text, "evaluation": performance_evaluation}


def evaluate_performance(revenue, leads, tours, applications, averages):
    performance_statements = []
    if revenue >= averages['revenue'] * 1.1:
        performance_statements.append("Outstanding revenue performance.")
    elif revenue < averages['revenue']:
        performance_statements.append("Revenue performance is below average.")

    if leads >= averages['leads'] * 1.1:
        performance_statements.append("Excellent job in lead acquisition.")
    elif leads < averages['leads']:
        performance_statements.append("Lead acquisition is below average.")

    if tours >= averages['tours'] * 1.1:
        performance_statements.append("Tours booked are impressive.")
    elif tours < averages['tours']:
        performance_statements.append("Tours booked are below expectations.")

    if applications >= averages['applications'] * 1.1:
        performance_statements.append("Applications processed are excellent.")
    elif applications < averages['applications']:
        performance_statements.append("Applications processed are lower than expected.")

    return " ".join(performance_statements) or "The performance metrics indicate room for improvement."


# API Endpoints

# 1. Home route that shows a form for user input
@app.route('/')
def home():
    return render_template('index.html')


# User Performance Route
@app.route('/user_performance')
def user_performance():
    return render_template('user_performance.html')


@app.route('/select_performance', methods=['POST'])
def select_performance():
    performance_type = request.form['performance_type']

    if performance_type == 'user':
        return render_template('index.html', performance_type='user')
    elif performance_type == 'team':
        # Call the team performance API or function
        team_performance = get_team_summary(data)
        return render_template('index.html', performance_type='team',
                               team_performance_summary=team_performance['team_performance_summary'])
    elif performance_type == 'trends':
        time_period = request.args.get('time_period', 'monthly')
        result = analyze_performance_trends(data, time_period)

        # Pass the result to the template
        return render_template('index.html', performance_type='trends', result=result)



@app.route('/team_performance')
def get_team_performance():
    result = get_team_summary(data)
    return jsonify(result)


# 2. Route to get feedback based on employee name from form submission
@app.route('/get_feedback', methods=['POST'])
def get_employee_feedback():
    # Get employee name from form submission
    employee_name = request.form['employee_name']

    # Extract employee data
    employee_data = data[data['employee_name'] == employee_name]

    if employee_data.empty:
        return render_template('index.html', error=f"No data found for employee: {employee_name}")

    # Calculate team averages for comparison
    averages = calculate_averages(data)

    # Generate performance summary
    result = evaluate_individual(employee_data, averages)

    # Render the result in the template
    return render_template('index.html', result=result)




### Run the Flask Application

if __name__ == '__main__':
    app.run(debug=True)
