# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from datetime import datetime
import ruptures as rpt
from statsmodels.tsa.seasonal import seasonal_decompose
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BrentOilPricesEDA:
    """
    A class for performing exploratory data analysis (EDA) on Brent oil price data.
    
    Parameters
    ----------
    file_path : str
        Path to the CSV file containing the Brent oil price data with 'Date' and 'Price' columns.
    """
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
    
    def load_data(self):
        """
        Loads the CSV file into a DataFrame.
        
        Returns
        -------
        pd.DataFrame
            The loaded data.
        """
        start_time = datetime.now()
        try:
            self.data = pd.read_csv(self.file_path)
            logging.info("Data loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise
        end_time = datetime.now()
        logging.info(f"Data loading completed in {end_time - start_time}.")
        return self.data

    def format_date(self):
        """
        Converts the 'Date' column to datetime, handles invalid dates, and sets 'Date' as the index.
        Returns
        -------
        pd.DataFrame
            DataFrame with 'Date' as the index.
        """
        if self.data is None:
            logging.warning("Data not loaded. Please load data before calling format_date.")
            return None
        
        start_time = datetime.now()
        # Convert Date column to datetime format with error handling
        self.data['Date'] = pd.to_datetime(self.data['Date'], infer_datetime_format=True, errors='coerce')
        
        # Drop rows with invalid dates
        invalid_dates = self.data[self.data['Date'].isna()]
        if not invalid_dates.empty:
            logging.warning(f"Found {len(invalid_dates)} rows with invalid dates. Dropping these rows.")
            self.data = self.data.dropna(subset=['Date'])
        
        # Sort by date and reset index
        self.data = self.data.sort_values('Date').reset_index(drop=True)
        self.data.set_index('Date', inplace=True)
        
        end_time = datetime.now()
        logging.info(f"Date formatting completed in {end_time - start_time}.")
        return self.data

    def describe_data(self):
        """
        Provides descriptive statistics of the data.
        Returns
        -------
        pd.DataFrame
            Summary statistics of the data.
        """
        if self.data is None:
            logging.warning("Data not loaded. Please load data before calling describe_data.")
            return None
        logging.info("Generating descriptive statistics.")
        return self.data.describe().round(2)

    def plot_time_series(self):
        """
        Plots the time series of Brent oil prices.
        """
        if self.data is None:
            logging.warning("Data not loaded. Please load data before calling plot_time_series.")
            return
        
        plt.figure(figsize=(14, 6))
        plt.plot(self.data.index, self.data['Price'], color='blue')
        plt.title("Brent Oil Prices Over Time")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.show()
        logging.info("Time series plot generated successfully.")
    def seasonal_decomposition(self):
        """
        Decomposes the time series of Brent oil prices into trend, seasonal, and residual components
        using additive decomposition and plots the results.
        """
        if self.data is None:
            logging.warning("Data not loaded. Please load data before calling seasonal_decomposition.")
            return
        
        logging.info("Performing seasonal decomposition.")

        # Decompose the time series to analyze trend and seasonality
        decomposition = seasonal_decompose(self.data['Price'], model='additive', period=30)
        
        # Plot the decomposition
        plt.figure(figsize=(14, 10))
        decomposition.plot()
        plt.suptitle("Seasonal Decomposition of Brent Oil Prices", fontsize=10)
        plt.show()

    def plot_acf_pacf(self, column='Price', lags=30):
        """
        Plots the ACF and PACF for the specified column.
        
        Parameters
        ----------
        column : str, optional
            The column name for which ACF and PACF are to be plotted (default is 'Price').
        lags : int, optional
            The number of lags to include in the ACF and PACF plots (default is 30).
        """
        if self.data is None:
            logging.warning("Data not loaded. Please load data before calling plot_acf_pacf.")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        plot_acf(self.data[column], lags=lags, ax=ax1)
        plot_pacf(self.data[column], lags=lags, ax=ax2)
        plt.show()
        logging.info("ACF and PACF plots generated successfully.")

    def plot_histogram(self, column='Price', cmap='viridis'):
       
       if self.data is None:
        logging.warning("Data not loaded. Please load data before caling plot_histogram.")
       return

    plt.figure(figsize=(10, 6))

    # Generate histogram values
    hist_values, bins, patches = plt.hist(self.data[column], bins=20, edgecolor='black', alpha=0.7)

    # Apply colormap to each bin
    cmap = plt.get_cmap(cmap)
    for i, patch in enumerate(patches):
        patch.set_facecolor(cmap(i / len(patches)))

    # Calculate statistics
    mean_value = self.data[column].mean()
    median_value = self.data[column].median()
    min_value = self.data[column].min()
    max_value = self.data[column].max()

    # Add vertical lines for mean, median, min, and max
    plt.axvline(mean_value, color='red', linestyle='--', label=f'Mean: {mean_value:.2f}')
    plt.axvline(median_value, color='yellow', linestyle='--', label=f'Median: {median_value:.2f}')
    plt.axvline(min_value, color='green', linestyle='--', label=f'Min: {min_value:.2f}')
    plt.axvline(max_value, color='blue', linestyle='--', label=f'Max: {max_value:.2f}')

    # Adding KDE
    sns.kdeplot(self.data[column], color='black', linewidth=2, label='KDE')

    # Final plot adjustments
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.title(f'Histogram for {column}')
    plt.legend()
    plt.grid(axis='y', alpha=0.75)  # Add grid for better readability
    plt.show()

    logging.info("Histogram plot generated successfully with statistics and colormap.")


    def plot_cusum(self, column_name='Price'):
        """
        Calculate and plot the CUSUM values for the specified column.
        """
        # Calculate the CUSUM values
        cusum_values = np.cumsum(self.data[column_name] - self.data[column_name].mean())
        
        # Plot the CUSUM values
        plt.figure(figsize=(14, 7))
        plt.plot(self.data.index, cusum_values, label='CUSUM', color='blue')
        plt.axhline(y=0, color='red', linestyle='--')
        plt.xlabel('Date')
        plt.ylabel('CUSUM Value')
        plt.title('CUSUM Analysis')
        plt.legend()
        plt.show()
    def change_point_analysis(self):
        """
        Performs change point analysis on the 'Price' data using the ruptures library.
        Plots the Brent oil prices and highlights detected change points.
        """
        if self.data is None:
            logging.warning("Data not loaded. Please load data before calling change_point_analysis.")
            return
        
        logging.info("Performing change point analysis.")
        
        # Prepare the price data as an array
        price_series = self.data['Price'].values

        # Define the model as 'rbf' for kernel-based change point detection
        model = "rbf"
        algo = rpt.Pelt(model=model).fit(price_series)

        # Increase the penalty to reduce the number of change points
        change_points = algo.predict(pen=15)  # we can adjust the penalty to find significant changes

        # Plotting the results
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, price_series, label="Brent Oil Prices", color='blue')

        # Plot each change point, with only one label in the legend
        for i, cp in enumerate(change_points):
            if i == 0:  # Add label only for the first change point
                plt.axvline(self.data.index[cp - 1], color='red', linestyle='--', label="Change Point")
            else:
                plt.axvline(self.data.index[cp - 1], color='red', linestyle='--')

        plt.legend()
        plt.title("Change Point Analysis on Brent Oil Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()
    def check_stationarity(self):
        """
        Checks the stationarity of the 'Price' column using the Augmented Dickey-Fuller (ADF) test.
        
        If the series is non-stationary (p > 0.05), applies first differencing and plots the differenced series.
        """
        if self.data is None:
            logging.warning("Data not loaded. Please load data before calling check_stationarity.")
            return
        
        logging.info("Performing Augmented Dickey-Fuller test for stationarity.")
        result = adfuller(self.data['Price'])
        logging.info(f"ADF Statistic: {result[0]}")
        logging.info(f"p-value: {result[1]}")
        
        if result[1] > 0.05:
            logging.info("Data is non-stationary; applying first differencing.")
            self.data['price_diff'] = self.data['Price'].diff()

            # Drop the NaN value resulting from differencing
            plt.figure(figsize=(14, 6))
            plt.plot(self.data.index[1:], self.data['price_diff'].dropna(), color='green')  # Use dropna() to align lengths
            plt.title('Differenced Brent Oil Prices')
            plt.xlabel("Date")
            plt.ylabel("Differenced Price")
            plt.show()
        else:
            logging.info("Data is stationary; proceed without differencing.")
            