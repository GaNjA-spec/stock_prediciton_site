from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os

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

def plot_stock_graph(symbol, data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], data['Close'], label=f"{symbol} Closing Price", color='blue')
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.title(f"{symbol} Stock Price Trend")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.7)
    plt.xticks(rotation=45)
    graph_file = f"static/{symbol}_graph.png"
    plt.savefig(graph_file)
    return graph_file

def predict_next_closing_price(data):
    X = data.index.values.reshape(-1, 1)
    y = data['Close'].values

    model = LinearRegression()
    model.fit(X, y)

    next_day = len(data)
    next_closing_price = model.predict([[next_day]])

    return next_closing_price[0]

@app.route('/')
def index():
    return render_template('index.html', symbols=common_stock_symbols)

@app.route('/stock', methods=['POST'])
def stock():
    symbol = request.form['symbol']
    period = request.form['period']
    stock_data = get_stock_data(symbol, period)
    if stock_data:
        graph_file = plot_stock_graph(symbol, pd.DataFrame(stock_data))
        next_closing_price = predict_next_closing_price(pd.DataFrame(stock_data))
        return render_template('stock.html', symbol=symbol, data=stock_data, graph_file=graph_file, next_closing_price=next_closing_price)
    else:
        return render_template('error.html', message=f"Error fetching data for {symbol}")

if __name__ == "__main__":
    app.run(debug=True)
