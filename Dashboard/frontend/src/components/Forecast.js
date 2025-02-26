import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const PriceChart = () => {
  const [priceData, setPriceData] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/data/forecast")
      .then((response) => {
        setPriceData(response.data);
      })
      .catch((error) => console.error("Error fetching price data:", error));
  }, []);

  return (
    <div className="chart-container">
      <h2>Historical Brent Oil Prices</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={priceData}>
          <XAxis dataKey="Date" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="PredictedPrice"
            stroke="#82ca9d"
          />{" "}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PriceChart;
