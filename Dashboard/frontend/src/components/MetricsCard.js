import React from "react";
import { Card, CardContent, Typography } from "@mui/material";

const MetricsCard = () => {
  return (
    <Card className="metrics-card">
      <CardContent>
        <Typography variant="h5">Model Performance</Typography>
        <Typography variant="body1">RMSE: 2.5</Typography>
        <Typography variant="body1">MAE: 1.8</Typography>
      </CardContent>
    </Card>
  );
};

export default MetricsCard;
