from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go
import os

app = Flask(__name__)

def get_stock_data(symbol, period="1mo"):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return data.reset_index()
    except Exception as e:
        return None

def plot_stock_graph(symbol, data):
    trace = go.Scatter(x=data['Date'], y=data['Close'], mode='lines+markers', name=f"{symbol} Closing Price")

    layout = go.Layout(
        title=f"{symbol} Stock Price Trend",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Price (USD)"),
        hovermode='closest'
    )

    fig = go.Figure(data=[trace], layout=layout)
    graph_file = f"static/{symbol}_graph.html"
    fig.write_html(graph_file, auto_open=False)
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
    return render_template('index.html')

@app.route('/stock', methods=['POST'])
def stock():
    symbol = request.form['symbol']
    period = request.form['period']
    stock_data = get_stock_data(symbol, period)
    if stock_data is not None:
        graph_file = plot_stock_graph(symbol, stock_data)
        next_closing_price = predict_next_closing_price(stock_data)
        return render_template('stock.html', symbol=symbol, graph_file=graph_file, next_closing_price=next_closing_price)
    else:
        return render_template('error.html', message=f"Error fetching data for {symbol}")

if __name__ == "__main__":
    app.run(debug=True)
