import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import pypfopt
from pypfopt import risk_models
from pypfopt import plotting
from pypfopt import expected_returns
from pypfopt import EfficientFrontier


class MeanVarianceOptimization:
    def __init__(self, stocks, start_date, end_date):
        ohlc = yf.download(stocks, start=start_date, end=end_date)
        self.stocks = stocks
        self.prices = ohlc["Adj Close"].dropna(how="all")
        
    def cov(self):
        cov = risk_models.CovarianceShrinkage(self.prices).ledoit_wolf()
        return cov

    def expected_returns(self):
        mu = expected_returns.capm_return(self.prices)
        return mu

    def weights(self):
        er = self.expected_returns()
        cov = self.cov()

        ef = EfficientFrontier(er, cov, weight_bounds=(None, None))
        ef.min_volatility()
        weights = ef.clean_weights()
        return weights