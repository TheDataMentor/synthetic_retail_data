import pandas as pd
import numpy as np

def load_data(file_path):
    return pd.read_csv(file_path)

def calculate_summary_statistics(df):
    summary = df.groupby('Category').agg({
        'Sales': ['mean', 'median', 'std'],
        'Quantity': ['mean', 'median', 'std'],
        'Profit': ['mean', 'median', 'std']
    })
    return summary

def identify_top_products(df, n=10):
    return df.groupby('Product ID')['Sales'].sum().nlargest(n)

def analyze_seasonality(df):
    df['Month'] = pd.to_datetime(df['Order Date']).dt.month
    monthly_sales = df.groupby('Month')['Sales'].mean()
    return monthly_sales

# Add more analysis functions as needed
