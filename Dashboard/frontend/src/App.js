// App.js
import React, { useState } from "react";
import PriceChart from "./components/PriceChart";
import EventFilter from "./components/EventFilter";
import MetricsCard from "./components/MetricsCard";
import Forecast from "./components/Forecast";
import { DateRangePicker } from "@mui/x-date-pickers-pro";
import { LocalizationProvider } from "@mui/x-date-pickers-pro";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { TextField } from "@mui/material";
import "./App.css";

function App() {
  const [selectedDateRange, setSelectedDateRange] = useState([null, null]);
  const [selectedEventType, setSelectedEventType] = useState("all");

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <div className="App">
        <header className="App-header">
          <h1>Brent Oil Price Dashboard</h1>
        </header>
        <div className="card-container">
          <EventFilter
            className="mt-10"
            selectedEventType={selectedEventType}
            setSelectedEventType={setSelectedEventType}
          />
          <DateRangePicker
            startText="Start Date"
            endText="End Date"
            value={selectedDateRange}
            onChange={(newValue) => setSelectedDateRange(newValue)}
            renderInput={(startProps, endProps) => (
              <>
                <TextField {...startProps} />
                <span style={{ margin: "0 10px" }}> to </span>
                <TextField {...endProps} />
              </>
            )}
          />
          <MetricsCard />
        </div>
        <div className="container">
          <div className="chart-column">
            <PriceChart
              selectedDateRange={selectedDateRange}
              selectedEventType={selectedEventType}
            />
          </div>
          <div className="forecast-column">
            <Forecast />
          </div>
        </div>
      </div>
    </LocalizationProvider>
  );
}

export default App;
