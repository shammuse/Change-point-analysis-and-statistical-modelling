# Step 2: Import the libraries
import wbdata
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class WorldDataAnalysis:
    def __init__(self):
        # Updated indicators dictionary with new indicators
        self.indicators = {
            "NY.GDP.MKTP.KD.ZG": "GDP Growth (%)",
            "FP.CPI.TOTL.ZG": "Inflation Rate (%)",
            "SL.UEM.TOTL.ZS": "Unemployment Rate (%)",
            "PA.NUS.FCRF": "Exchange Rate (USD)"
        }
        self.start_date = datetime(1986, 5, 20)
        self.end_date = datetime(2024, 9, 30)
        self.world_data = None

    def fetch_world_data(self):
        """Fetch world data for selected indicators from the World Bank API."""
        try:
            print("Fetching world data...")
            self.world_data = wbdata.get_dataframe(self.indicators, country="WLD")
            print("Fetch complete. Data type:", type(self.world_data))

            if isinstance(self.world_data, pd.DataFrame):
                self.world_data.reset_index(inplace=True)
                
                # Convert the 'date' column to datetime
                self.world_data['date'] = pd.to_datetime(self.world_data['date'])
                
                # Filter based on the date column
                self.world_data = self.world_data[(self.world_data['date'] >= self.start_date) & 
                                                (self.world_data['date'] <= self.end_date)]
                print("World data fetched and filtered by date successfully.")
                print(self.world_data.head())  # Preview the filtered data

                # Save to CSV
                self.world_data.to_csv('world_data.csv', index=False)
                print("Data saved to 'world_data.csv'.")

            else:
                print("Unexpected output format:", type(self.world_data))
                print("Response content:", self.world_data)

        except Exception as e:
            print("Error fetching world data:", e)


    def resample_to_daily(self):
        """Resample annual world data to daily frequency and forward-fill."""
        if self.world_data is not None:
            self.world_data.set_index('date', inplace=True)  # Set date as index for resampling
            self.world_data_daily = self.world_data.resample('D').ffill()
            print("World data resampled to daily frequency.")
            print(self.world_data_daily.head())  # Display the first few rows for inspection
        else:
            print("World data not loaded. Run fetch_world_data() first.")

    def load_oil_prices_from_csv(self, file_path):
        """Load daily oil price data from a CSV file."""
        try:
            self.oil_prices = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
            print("Oil prices loaded successfully.")
            print(self.oil_prices.head())  # Display the first few rows for inspection
        except Exception as e:
            print("Error loading oil prices from CSV:", e)

    def merge_data(self):
        """Merge daily world data with daily oil prices, keeping only the dates available in oil prices."""
        if self.world_data_daily is not None and hasattr(self, 'oil_prices'):
            # Perform a right join to retain only dates from oil prices data
            self.merged_data = self.world_data_daily.merge(self.oil_prices, left_index=True, right_index=True, how="right")
            print("Data merged successfully, maintaining only dates from oil prices data.")
            print(self.merged_data.head())  # Display the first few rows for inspection
            
            # Save the merged data to CSV
            self.merged_data.to_csv('merged_data.csv', index=True)
            print("Merged data saved to 'merged_data.csv'.")
        else:
            print("Data not prepared. Run resample_to_daily() and load_oil_prices_from_csv() first.")


    def calculate_correlations(self):
        """Calculate and display the correlation matrix."""
        if hasattr(self, 'merged_data'):
            correlation_matrix = self.merged_data.corr()
            plt.figure(figsize=(8, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", center=0)
            plt.title("Correlation Matrix of Global GDP, Inflation, Unemployment, Exchange Rate, and Oil Price (Daily Data)")
            plt.show()
        else:
            print("Merged data not available. Run merge_data() first.")

    def specific_correlation(self, indicator1, indicator2):
        """Calculate the correlation between two specific indicators."""
        if hasattr(self, 'merged_data') and indicator1 in self.merged_data.columns and indicator2 in self.merged_data.columns:
            correlation = self.merged_data[indicator1].corr(self.merged_data[indicator2])
            print(f"Correlation between {indicator1} and {indicator2}: {correlation}")
        else:
            print(f"Indicators not available in merged data. Available indicators are: {list(self.merged_data.columns)}")
