import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from src.data_analysis import load_data, calculate_summary_statistics, identify_top_products

# Load the data
df = load_data('data/synthetic_superstore_data.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('Synthetic Superstore Data Dashboard'),
    
    dcc.Graph(id='sales-trend'),
    
    dcc.Graph(id='category-distribution'),
    
    dcc.Graph(id='top-products')
])

@app.callback(
    Output('sales-trend', 'figure'),
    Input('sales-trend', 'id')
)
def update_sales_trend(id):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    daily_sales = df.groupby('Order Date')['Sales'].sum().reset_index()
    fig = px.line(daily_sales, x='Order Date', y='Sales', title='Daily Sales Trend')
    return fig

@app.callback(
    Output('category-distribution', 'figure'),
    Input('category-distribution', 'id')
)
def update_category_distribution(id):
    category_sales = df.groupby('Category')['Sales'].sum().reset_index()
    fig = px.bar(category_sales, x='Category', y='Sales', title='Sales by Product Category')
    return fig

@app.callback(
    Output('top-products', 'figure'),
    Input('top-products', 'id')
)
def update_top_products(id):
    top_products = identify_top_products(df)
    fig = px.bar(top_products.reset_index(), x='Product ID', y='Sales', title='Top 10 Products by Sales')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
