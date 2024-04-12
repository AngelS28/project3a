from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # Get form inputs
    symbol = request.form['symbol']
    chart_type = request.form['chart_type']
    function = request.form['time_series']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    # Call the main function with form inputs
    plot = main(symbol, chart_type, function, start_date, end_date)

    return render_template('result.html', plot=plot)

# Function to query Alpha Vantage API
def query_alpha_vantage(symbol, function, start_date, end_date):
    api_key = "UT2CFA26ZELQE5H2" 
    base_url = "https://www.alphavantage.co/query"

    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "full",  # Retrieve full data for the range selected
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    return data

# Function to plot the graph
def plot_graph(dates, values, chart_type):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values)
    plt.title(f"Stock Data ({chart_type})")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plot_path = "/static/plot.png"
    plt.savefig('.' + plot_path)
    plt.close()
    return plot_path

# Main function (enter inputs)
def main(symbol, chart_type, function, start_date, end_date):
    choice = function
    # Query Alpha Vantage API
    if choice != "Time Series (5min)":
        data = query_alpha_vantage(symbol, function, start_date, end_date)
    else:
        interval = "5min"
        data = query_alpha_vantage_intraday(symbol,function,start_date,end_date,interval)

    # Extract dates and values 
    dates = []
    values = []
    for date, value in data[choice].items():
        dates.append(date)
        values.append(float(value["4. close"]))  # Assuming closing price is needed

    # Plot the graph
    plot_path = plot_graph(dates, values, chart_type)
    return plot_path

if __name__ == '__main__':
    app.run(debug=True)
