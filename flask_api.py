from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    symbol = request.form['symbol']
    chart_type = request.form['chart_type']
    time_series = request.form['time_series']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    # Call your existing functions with the received parameters

    return render_template('result.html', data=data)  # Pass data to the result template

if __name__ == '__main__':
    app.run(debug=True)
