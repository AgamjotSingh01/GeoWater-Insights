'use client'
import React, { useEffect, useState } from "react";

export default function Result() {
    const [predictionData, setPredictionData] = useState(null);

    useEffect(() => {
        const data = localStorage.getItem("predictionData");
        if (data) {
            setPredictionData(JSON.parse(data));
        }
    }, []);

    return (
        <div className="container">
            <h1>Groundwater Prediction Results</h1>
            {predictionData ? (
                <div style={{ color: "white" }}>
                    <p><strong>Predicted Groundwater Level (Avg):</strong> {predictionData.Prediction} meters</p>
                    <p><strong>Mean Absolute Error (MAE):</strong> {predictionData.MAE}</p>
                    <p><strong>Mean Squared Error (MSE):</strong> {predictionData.MSE}</p>
                    <p><strong>R² Score:</strong> {predictionData["R²"]}</p>

                    {/* Show the groundwater level array */}
                    <h3>Groundwater Level Predictions:</h3>
                    <ul>
                        {predictionData.Groundwater_Level.map((level, index) => (
                            <li  key={index}>Reading {index + 1}: {level} meters</li>
                        ))}
                    </ul>

                    {/* Graph Display */}
                    <h3 >Prediction Performance Graph:</h3>
                    <img src={`data:image/png;base64,${predictionData.Graph}`} alt="Groundwater Prediction Graph" />
                </div>
            ) : (
                <p>Loading prediction data...</p>
            )}
        </div>
    );
}
