# app.py
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load sample data
historical_data = pd.read_csv('data/BrentOilprices.csv')
mergedData = pd.read_csv('data/merged_data.csv')
events_data = pd.read_csv('data/world_data.csv')
forecast_data = pd.read_csv('data/world_data.csv')


@app.route('/api/data/merged_oil_price_history', methods=['GET'])
def get_merged_oil_price_history():
    return jsonify(mergedData.to_dict(orient='records'))


@app.route('/api/data/historical-prices', methods=['GET'])
def get_historical_prices():
    return jsonify(historical_data.to_dict(orient='records'))

@app.route('/api/data/events', methods=['GET'])
def get_events():
    return jsonify(events_data.to_dict(orient='records'))

@app.route('/api/data/forecast', methods=['GET'])
def get_forecast():
    return jsonify(forecast_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
