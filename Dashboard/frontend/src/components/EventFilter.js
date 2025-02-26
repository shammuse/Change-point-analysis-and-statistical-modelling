import React, { useState, useEffect } from "react";
import { TextField, MenuItem } from "@mui/material";
import axios from "axios";

const EventFilter = ({ selectedEventType, setSelectedEventType }) => {
  const [eventTypes, setEventTypes] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/data/merged_oil_price_history")
      .then((response) => {
        // Extract unique event types from data
        const uniqueEventTypes = [
          ...new Set(response.data.map((item) => item.event_type)),
        ];
        setEventTypes(uniqueEventTypes);
      })
      .catch((error) => console.error("Error fetching event types:", error));
  }, []);

  return (
    <div className="filter-container">
      <h5>Select the Label</h5>
      <TextField
        select
        label="Filter by Event Type"
        variant="outlined"
        fullWidth
        value={selectedEventType}
        onChange={(e) => setSelectedEventType(e.target.value)}
      >
        <MenuItem value="all">All</MenuItem>
        {eventTypes.map((type) => (
          <MenuItem key={type} value={type}>
            {type}
          </MenuItem>
        ))}
      </TextField>
    </div>
  );
};

export default EventFilter;
