import os
import pygal
import csv
import base64
from flask import Flask, render_template, request
from markupsafe import Markup 
import requests

#Initialize and configure Flask
app = Flask(__name__, static_folder='static')

app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'

API_KEY = "8G1UIII9UVSTDVKT"

#Define routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            #Extract form data
            ticker_symbol = request.form['ticker_symbol'].upper()
            chart_type = int(request.form['chart_type'])
            chart_time_series = request.form['chart_time_series']
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            #Get stock data from API
            stock_data = get_stock_data(ticker_symbol, chart_time_series)
            print("Stock data:", stock_data)

            #Generate chart
            if stock_data:
                chart_svg = make_graph(stock_data, chart_type, chart_time_series, start_date, end_date)
                return render_template('index.html', chart_generated=True, chart_svg=Markup(chart_svg))
            else:
                return render_template('index.html', error_message="Error fetching stock data.")
        #Error checking
        except Exception as e:
            return render_template('index.html', error_message=f"Error: {e}")

    stock_symbols = get_stock_symbols()

    return render_template('index.html', stock_symbols=stock_symbols)

#Get ticker symbols from csv
def get_stock_symbols():
    stock_symbols = []
    with open('stocks.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stock_symbols.append(row['Symbol'])
    return stock_symbols

#Stock data from API
def get_stock_data(symbol, time_series):
    base_url = "https://www.alphavantage.co/query"
    function = f'TIME_SERIES_{"INTRADAY" if time_series == "5" else "DAILY"}'
    
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": API_KEY,
        "interval": "5min" if time_series == "5" else None
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching data. Status Code: {response.status_code}")
        print(f"API Response: {response.text}")
        return None

#Create graph
def make_graph(stock_data, chart_type, chart_time_series, start_date, end_date):
    time_series_key = 'Time Series (5min)' if chart_time_series == '5' else 'Time Series (Daily)'
    
    if time_series_key not in stock_data:
        print(f"No data available for the specified time period: {start_date} to {end_date}")
        return
    
    ticker = stock_data['Meta Data']['2. Symbol']

    opening = []
    highs = []
    lows = []
    closing = []
    dates = []

    for date, values in stock_data[time_series_key].items():
        if start_date <= date <= end_date:
            dates.append(date)
            opening.append(float(values["1. open"]))
            highs.append(float(values["2. high"]))
            lows.append(float(values["3. low"]))
            closing.append(float(values["4. close"]))

    if not dates:
        print("There Was No Data Available For Your Input")
    else:
        if chart_type == 2:
            chart = pygal.Line()
        else:
            chart = pygal.Bar()
        chart.title = f'Stock Data for {ticker}: {start_date} to {end_date}'
        chart.x_labels = dates
        chart.add('Opening', opening)
        chart.add('High', highs)
        chart.add('Low', lows)
        chart.add('Closing', closing)

        chart_svg = chart.render(is_unicode=True)

        return chart_svg

#Run Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)