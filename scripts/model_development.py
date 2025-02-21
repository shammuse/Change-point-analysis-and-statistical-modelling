import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima_model import ARIMA
# from keras.layers import LSTM

class ModelBuilder:
    def __init__(self):
        self.model = None

    def split_data(self, data, train_size=0.8):
        try:
            # Split the data into training and testing sets
            train_size = int(len(data) * train_size)
            train_data = data[:train_size]
            test_data = data[train_size:]
            return train_data, test_data
        except Exception as e:
            logging.error(f"Error in splitting data: {e}")
            return None, None
    # build ARIMA model
    def build_arima_model(self, train_data, test_data):
        try:
            # Initialize the model
            self.model = ARIMA(train_data, order=(1, 1, 1))

            # Fit the model
            self.model_fit = self.model.fit()

            # Make predictions
            y_pred = self.model_fit.forecast(steps=len(test_data))[0]

            # Calculate the R2 score
            r2 = r2_score(test_data, y_pred)

            return self.model_fit, r2
        except Exception as e:
            logging.error(f"Error in building ARIMA model: {e}")
            return None, None
    def LSTM_model(self, train_data, test_data):
        try:
            # Initialize the model
            self.model = LSTM()

            # Fit the model
            self.model.fit(train_data)

            # Make predictions
            y_pred = self.model.predict(test_data)

            # Calculate the R2 score
            r2 = r2_score(test_data, y_pred)

            return self.model, r2
        except Exception as e:
            logging.error(f"Error in building LSTM model: {e}")
            return None, None