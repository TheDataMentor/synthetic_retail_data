import numpy as np
import pandas as pd
from scipy.stats import poisson
from datetime import datetime, timedelta
from numba import jit

# Set random seed for reproducibility
np.random.seed(42)

# Define parameters
start_date = datetime(2021, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Simplified product hierarchy for faster processing
product_hierarchy = {
    'Furniture': ['Chairs', 'Tables', 'Storage'],
    'Office Supplies': ['Writing', 'Paper', 'Organizing'],
    'Technology': ['Computers', 'Peripherals', 'Accessories']
}

# Other variables (cities, customer_segments, etc.) remain the same

@jit(nopython=True)
def fast_calculate_price(base_price, lifecycle_factor, economic_factor, seasonal_factor, day_factor, category_factor):
    return base_price * lifecycle_factor * economic_factor * seasonal_factor * day_factor * category_factor

@jit(nopython=True)
def fast_calculate_quantity(base_price, final_price, price_sensitivity):
    price_ratio = final_price / base_price
    base_lambda = 10
    lambda_param = base_lambda * (1 / price_ratio) ** price_sensitivity
    return max(1, poisson.rvs(lambda_param))

def generate_products(product_hierarchy):
    products = []
    for category, product_types in product_hierarchy.items():
        for product_type in product_types:
            for i in range(np.random.randint(2, 6)):
                products.append({
                    'Product ID': f'P{len(products) + 1}',
                    'Category': category,
                    'Product Type': product_type,
                    'Product Name': f'{product_type} {i + 1}',
                    'Base Price': np.random.uniform(10, 300),
                    'Launch Date': np.random.choice(date_range),
                    'Price Sensitivity': np.random.uniform(0.5, 2.0),
                })
    return pd.DataFrame(products)

def generate_customer_base(num_customers=1000):
    segments = np.random.choice(['Consumer', 'Corporate', 'Home Office'], size=num_customers, p=[0.6, 0.3, 0.1])
    return pd.DataFrame({
        'Customer ID': [f'C{i+1}' for i in range(num_customers)],
        'Customer Name': [f'Customer {i+1}' for i in range(num_customers)],
        'Segment': segments,
        'Loyalty Score': np.random.randint(1, 101, size=num_customers)
    })

def generate_synthetic_data():
    products_df = generate_products(product_hierarchy)
    customers_df = generate_customer_base()
    
    data = []
    stock_levels = {product: np.random.randint(50, 201) for product in products_df['Product ID']}
    
    for date in date_range:
        # Vectorized operations for price calculation
        lifecycle_factors = np.random.uniform(0.98, 1.02, len(products_df))
        economic_factors = np.random.uniform(0.99, 1.01, len(products_df))
        seasonal_factors = np.random.uniform(0.8, 1.2, len(products_df))
        day_factors = np.where(date.weekday() in [5, 6], 0.95, 1)
        category_factors = np.where(products_df['Category'] == 'Furniture', 1.2,
                                    np.where(products_df['Category'] == 'Office Supplies', 1.1, 1.3))
        
        base_prices = products_df['Base Price'].values
        final_prices = fast_calculate_price(base_prices, lifecycle_factors, economic_factors, 
                                            seasonal_factors, day_factors, category_factors)
        
        # Generate transactions
        num_transactions = np.random.randint(50, 201)
        for _ in range(num_transactions):
            customer = customers_df.iloc[np.random.randint(len(customers_df))]
            num_products = np.random.randint(1, 6)
            
            for _ in range(num_products):
                product_idx = np.random.randint(len(products_df))
                product = products_df.iloc[product_idx]
                
                if stock_levels[product['Product ID']] <= 0:
                    continue
                
                loyalty_discount = min(customer['Loyalty Score'] * 0.001, 0.1)
                price = final_prices[product_idx] * (1 - loyalty_discount)
                
                quantity = fast_calculate_quantity(product['Base Price'], price, product['Price Sensitivity'])
                quantity = max(1, min(quantity, stock_levels[product['Product ID']]))
                
                revenue = price * quantity
                cost = product['Base Price'] * 0.6 * quantity
                profit = revenue - cost
                
                stock_levels[product['Product ID']] -= quantity
                
                data.append({
                    'Transaction ID': f'T{len(data) + 1}',
                    'Order Date': date,
                    'Customer ID': customer['Customer ID'],
                    'Product ID': product['Product ID'],
                    'Category': product['Category'],
                    'Product Type': product['Product Type'],
                    'Sales': revenue,
                    'Quantity': quantity,
                    'Unit Price': price,
                    'Profit': profit,
                })
        
        # Simplified restocking
        for product_id, stock in stock_levels.items():
            if stock < 20:
                stock_levels[product_id] += np.random.randint(50, 101)
    
    return pd.DataFrame(data)

# Generate and save the data
df = generate_synthetic_data()
df.to_csv('optimized_synthetic_data.csv', index=False)
print("Optimized synthetic dataset created and saved as 'optimized_synthetic_data.csv'.")
