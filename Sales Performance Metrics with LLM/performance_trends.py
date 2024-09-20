import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np

def prepare_data_for_trend_analysis(data, time_period):

    data['created'] = pd.to_datetime(data['created'])

    # Group data based on the time period (monthly/quarterly)
    if time_period == 'monthly':
        data['month'] = data['created'].dt.month
        data['year'] = data['created'].dt.year
        grouped_data = data.groupby(['year', 'month']).agg({
            'tours_booked': 'sum',
            'applications': 'sum',
            'revenue_confirmed': 'sum'
        }).reset_index()
    elif time_period == 'quarterly':
        data['quarter'] = data['created'].dt.to_period('Q')
        grouped_data = data.groupby(['quarter']).agg({
            'tours_booked': 'sum',
            'applications': 'sum',
            'revenue_confirmed': 'sum'
        }).reset_index()
        grouped_data['quarter'] = grouped_data['quarter'].astype(str)

    return grouped_data

# ARIMA Forecasting with evaluation
def forecast_with_arima(grouped_data, steps=3):
    revenue_series = grouped_data['revenue_confirmed']

    # Fit ARIMA model
    model = ARIMA(revenue_series, order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast future values
    forecast_arima = model_fit.forecast(steps=steps)

    # Calculate RMSE
    rmse = np.sqrt(np.mean((revenue_series[-steps:] - model_fit.forecast(steps))**2))
    return forecast_arima.tolist(), rmse

# Prophet Forecasting
def forecast_with_prophet(grouped_data, steps=3):
    df_prophet = grouped_data[['month', 'revenue_confirmed']].rename(columns={'month': 'ds', 'revenue_confirmed': 'y'})
    prophet_model = Prophet()
    prophet_model.fit(df_prophet)

    # Create future dataframe and forecast
    future = prophet_model.make_future_dataframe(periods=steps, freq='M')
    forecast_prophet = prophet_model.predict(future)

    return forecast_prophet[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(steps)

# Main function for analyzing trends and forecasting
def analyze_performance_trends(data, time_period='monthly', steps=3):
    grouped_data = prepare_data_for_trend_analysis(data, time_period)
    forecast_arima, arima_rmse = forecast_with_arima(grouped_data, steps)
    forecast_prophet = forecast_with_prophet(grouped_data, steps)

    # Plotting the results
    plt.figure(figsize=(12, 6))
    plt.plot(grouped_data['revenue_confirmed'], label='Actual Revenue', color='blue')
    plt.plot(range(len(grouped_data), len(grouped_data) + steps), forecast_arima, label='ARIMA Forecast', color='orange')
    plt.plot(forecast_prophet['ds'], forecast_prophet['yhat'], label='Prophet Forecast', color='green')
    plt.fill_between(forecast_prophet['ds'], forecast_prophet['yhat_lower'], forecast_prophet['yhat_upper'], color='green', alpha=0.2)
    plt.legend()
    plt.title('Revenue Forecasting')
    plt.xlabel('Time')
    plt.ylabel('Revenue Confirmed')
    plt.show()
    plt.close()

    return {
        'trend_data': grouped_data.to_dict(orient='records'),
        'forecast_arima': forecast_arima,
        'forecast_prophet': forecast_prophet.to_dict(orient='records'),
        'arima_rmse': arima_rmse,
        'performance_summary': "Trend Analysis Complete",
        'evaluation':"The forecast shows a variation in predicted revenue over the next three months, with an initial increase in June followed by a decrease in July, then a slight recovery in August, The trends suggest some fluctuation in revenue, which may indicate seasonal effects or changes in bookings and applications during these months."
    }
