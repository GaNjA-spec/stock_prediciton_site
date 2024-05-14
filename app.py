from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

common_stock_symbols = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc. (Google)",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla, Inc.",
    # Add more symbols and names as needed
}

def get_stock_data(symbol, period="1mo"):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return data.reset_index().to_dict(orient='records')
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html', symbols=common_stock_symbols)

@app.route('/stock', methods=['POST'])
def stock():
    symbol = request.form['symbol']
    period = request.form['period']
    stock_data = get_stock_data(symbol, period)
    if stock_data:
        return render_template('stock.html', symbol=symbol, data=stock_data)
    else:
        return render_template('error.html', message=f"Error fetching data for {symbol}")

if __name__ == "__main__":
    app.run(debug=True)
