from flask import Flask, render_template, request
import yfinance as yf
import numpy as np
import datetime as dt

app = Flask(__name__)

def get_data_yf(stock, startDate):
    data = yf.download(stock, startDate)['Close']
    returns = data.pct_change()
    meanReturns = returns.mean()
    return meanReturns

def monte_carlo_simulation(stock_symbol):
    endDate = dt.datetime.now()
    startDate = endDate - dt.timedelta(days=300)
    meanReturns = get_data_yf(stock_symbol, startDate)

    # Monte Carlo method
    mc_sims = 5  # number of simulations
    T = 100  # timeframe in days

    portfolio_sims = np.full(shape=(T, mc_sims), fill_value=0.0)

    initialPortfolio = 10000
    for m in range(mc_sims):
        
        dailyReturns = np.random.normal(meanReturns, np.std(meanReturns), T)
        portfolio_sims[:, m] = np.cumprod(dailyReturns + 1) * initialPortfolio

    final_portfolio_values = portfolio_sims[-1, :]

    mean_final_portfolio_value = np.mean(final_portfolio_values)
    std_final_portfolio_value = np.std(final_portfolio_values)
    return mean_final_portfolio_value, std_final_portfolio_value

@app.route('/')
def index():
    initial_portfolio_value = 10000 
    return render_template('index.html', initial_portfolio_value=initial_portfolio_value)


@app.route('/stock', methods=['POST'])
def stock():
    ticker = request.form['ticker']
    mean_portfolio_value, std_portfolio_value = monte_carlo_simulation(ticker.upper())
    return render_template('index.html', ticker=ticker.upper(), mean_portfolio_value=mean_portfolio_value, std_portfolio_value=std_portfolio_value)

if __name__ == '__main__':
    app.run(debug=True)

