This project architecture is a Flask-based web application designed to analyze sales performance data and provide summaries and trends. The application leverages external APIs (such as Hugging Face for summarization) and performs forecasting using machine learning libraries. 

Technologies Overview:
Backend: Flask (Python web framework)
Data Handling: Pandas (for reading and manipulating CSV data)
APIs: Hugging Face Inference API for text summarization
Machine Learning Models: ARIMA, Prophet (for forecasting and trend analysis)
Visualization: Matplotlib (for plotting trends and forecast results)
Templates: Flask's Jinja2 templating engine (for rendering HTML)

SETUP AND RUN INSTRUCTIONS!
Enviorment Used in this project is Pycharm.

First of All you will need to get your HugginsFace API KEY, It would take just a matter of time.
You can get it from this link https://huggingface.co/settings/tokens, you will have to SignUp First.
Then navigate to your Account, click on the Round Icon, From there Settings->Access Tokens-> Create New Token
Get YOUR_API_KEY and paste it where it is required in the code, one in main and once in team_performance
Run the following Command on the Terminal
pip install huggingface_hub
pip install -r requirements.txt

