// PriceChart.js
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
import { format, parseISO, isValid } from "date-fns"; // Import isValid to check date validity

const PriceChart = ({ selectedDateRange, selectedEventType }) => {
  const [priceData, setPriceData] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/data/merged_oil_price_history")
      .then((response) => {
        const formattedData = response.data.map((entry) => ({
          ...entry,
          Date: parseISO(entry.Date), // Parse ISO date format
        }));

        // Debug: Log the formatted data
        console.log("Formatted Price Data:", formattedData);

        // Filter out any entries with invalid dates
        const validData = formattedData.filter((entry) => isValid(entry.Date));
        setPriceData(validData);
      })
      .catch((error) => console.error("Error fetching price data:", error));
  }, []);

  // Filter data based on selected date range and event type
  const filteredData = priceData.filter((entry) => {
    const isWithinDateRange =
      (!selectedDateRange[0] || entry.Date >= selectedDateRange[0]) &&
      (!selectedDateRange[1] || entry.Date <= selectedDateRange[1]);
    const matchesEventType =
      selectedEventType === "all" || entry.event_type === selectedEventType;

    return isWithinDateRange && matchesEventType;
  });

  return (
    <div className="chart-container">
      <h2>Historical Brent Oil Prices</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={filteredData}>
          <XAxis
            dataKey="Date"
            // domain={["auto", "auto"]}
            tickFormatter={(date) =>
              isValid(date) ? format(date, "yyyy") : ""
            }
            //   ticks={priceData
            //     .map((entry) => entry.Date)
            //     .filter((_, index) => index % 4 === 0)}
          />
          <YAxis />
          <Tooltip
            labelFormatter={(label) =>
              isValid(new Date(label))
                ? `Date: ${format(new Date(label), "yyyy-MM-dd")}`
                : ""
            }
          />
          <Line
            type="monotone"
            dataKey="Price"
            stroke="#82ca9d"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PriceChart;
