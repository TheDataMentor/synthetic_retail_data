# Synthetic Data Generator for Superstore Sales

This project generates synthetic sales data for a fictional superstore, simulating real-world patterns and behaviors.

## Features
- Generate large-scale synthetic sales data
- Simulate various factors including seasonality, economic indicators, and customer behavior
- Analyze and visualize the generated data

## Installation
1. Clone this repository
2. Install required packages: `pip install -r requirements.txt`

## Project Stucture 

synthetic-data-project/
├── README.md
├── requirements.txt
├── data/
│   └── synthetic_data.csv
├── src/
│   ├── data_generation.py
│   ├── anomaly_detection.py
│   └── visualization.py
├── notebooks/
│   └── analysis.ipynb
├── tests/
│   ├── test_data_generation.py
│   └── test_anomaly_detection.py
├── results/
│   ├── arima_forecast.png
│   └── detected_anomalies.png
└── app/
    ├── app.py
    └── templates/
        └── index.html
## Usage
To generate synthetic data:
