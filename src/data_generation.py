# version one
import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define parameters
start_date = datetime(2021, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Expanded product hierarchy
product_hierarchy = {
    'Furniture': {
        'Seating': ['Office Chairs', 'Dining Chairs', 'Sofas', 'Stools'],
        'Tables': ['Desks', 'Dining Tables', 'Coffee Tables', 'Side Tables'],
        'Storage': ['Bookcases', 'Cabinets', 'Shelving Units'],
        'Beds': ['Bed Frames', 'Mattresses', 'Headboards']
    },
    'Office Supplies': {
        'Writing Instruments': ['Pens', 'Pencils', 'Markers', 'Highlighters'],
        'Paper Products': ['Notebooks', 'Printer Paper', 'Sticky Notes', 'Envelopes'],
        'Organizing': ['Binders', 'Folders', 'Filing Cabinets', 'Desk Organizers'],
        'Accessories': ['Staplers', 'Tape Dispensers', 'Scissors', 'Calculators']
    },
    'Technology': {
        'Computers': ['Laptops', 'Desktops', 'Tablets', 'All-in-One PCs'],
        'Peripherals': ['Monitors', 'Keyboards', 'Mice', 'Printers'],
        'Networking': ['Routers', 'Switches', 'Network Adapters'],
        'Accessories': ['Laptop Bags', 'Headphones', 'Webcams', 'External Hard Drives']
    }
}

sales_types = ['Regular', 'Promotion', 'Markdown']

# Create a holiday calendar (U.S. Bank Holidays + Back to School)
holidays = pd.to_datetime([
    # ... (same as before)
])

# Define cities and their population weights
cities = {
    'New York': 0.3, 'Los Angeles': 0.25, 'Chicago': 0.2, 'Houston': 0.15, 'Phoenix': 0.1
}

# Customer segments and their characteristics
customer_segments = {
    'Consumer': {'frequency': 0.6, 'avg_basket': 100},
    'Corporate': {'frequency': 0.3, 'avg_basket': 500},
    'Home Office': {'frequency': 0.1, 'avg_basket': 300}
}

# Product lifecycle
product_lifecycle = {
    'New': {'growth_rate': 0.02, 'max_age': 90},
    'Growth': {'growth_rate': 0.01, 'max_age': 180},
    'Mature': {'growth_rate': 0, 'max_age': 360},
    'Decline': {'growth_rate': -0.01, 'max_age': 90}
}

# Economic indicators
economic_indicators = {
    2021: {'gdp_growth': 0.02, 'unemployment': 0.06},
    2022: {'gdp_growth': 0.015, 'unemployment': 0.055},
    2023: {'gdp_growth': 0.01, 'unemployment': 0.05}
}

# Seasonal popularity factors
seasonal_popularity = {
    'Winter': {'Furniture': 0.8, 'Office Supplies': 1.0, 'Technology': 1.2},
    'Spring': {'Furniture': 1.2, 'Office Supplies': 1.0, 'Technology': 0.9},
    'Summer': {'Furniture': 0.9, 'Office Supplies': 1.3, 'Technology': 0.8},
    'Fall': {'Furniture': 1.1, 'Office Supplies': 1.2, 'Technology': 1.1}
}

def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

def generate_product_relationships():
    relationships = {}
    for category, subcategories in product_hierarchy.items():
        for subcategory, product_types in subcategories.items():
            for product_type in product_types:
                relationships[product_type] = {
                    'complements': random.sample(list(product_types), k=min(2, len(product_types))),
                    'substitutes': random.sample(list(product_types), k=min(2, len(product_types)))
                }
    return relationships

product_relationships = generate_product_relationships()

def generate_products(product_hierarchy):
    products = []
    for category, subcategories in product_hierarchy.items():
        for subcategory, product_types in subcategories.items():
            for product_type in product_types:
                for i in range(random.randint(2, 5)):  # 2-5 products per product type
                    product_id = f'P{len(products) + 1}'
                    base_price = np.random.uniform(10, 300)
                    price_sensitivity = np.random.uniform(0.5, 2.0)  # Price sensitivity factor
                    products.append({
                        'Product ID': product_id,
                        'Category': category,
                        'Subcategory': subcategory,
                        'Product Type': product_type,
                        'Product Name': f'{product_type} {i + 1}',
                        'Base Price': base_price,
                        'Launch Date': random.choice(date_range),
                        'Lifecycle Stage': 'New',
                        'Price Sensitivity': price_sensitivity,
                        'Promotion Fatigue': 0,
                        'Last Promotion Date': None
                    })
    return pd.DataFrame(products)

def update_product_lifecycle(product, current_date):
    age = (current_date - product['Launch Date']).days
    for stage, details in product_lifecycle.items():
        if age <= details['max_age']:
            product['Lifecycle Stage'] = stage
            break
    return product

def calculate_price(product, date, economic_indicators):
    base_price = product['Base Price']
    lifecycle_factor = 1 + product_lifecycle[product['Lifecycle Stage']]['growth_rate']
    
    # Economic factor
    year = date.year
    economic_factor = 1 + economic_indicators[year]['gdp_growth'] - economic_indicators[year]['unemployment'] / 2
    
    # Seasonal factor
    season = get_season(date)
    seasonal_factor = seasonal_popularity[season][product['Category']]
    
    # Day of week factor
    day_factor = 0.95 if date.weekday() in [5, 6] else 1  # Weekend discount
    
    # Category-specific factor
    category_factors = {'Furniture': 1.2, 'Office Supplies': 1.1, 'Technology': 1.3}
    category_factor = category_factors.get(product['Category'], 1)
    
    final_price = base_price * lifecycle_factor * economic_factor * seasonal_factor * day_factor * category_factor
    return round(final_price, 2)

def calculate_quantity(base_quantity, price_ratio, price_sensitivity):
    quantity_change = (1 - price_ratio) * price_sensitivity
    adjusted_quantity = base_quantity * (1 + quantity_change)
    return max(1, round(adjusted_quantity))

def adjust_quantity_for_related_products(base_quantity, product, cart_products):
    adjustment = 0
    for cart_product in cart_products:
        if product['Product Type'] in product_relationships[cart_product['Product Type']]['complements']:
            adjustment += random.uniform(0.1, 0.3) * base_quantity
        elif product['Product Type'] in product_relationships[cart_product['Product Type']]['substitutes']:
            adjustment -= random.uniform(0.1, 0.3) * base_quantity
    return max(1, round(base_quantity + adjustment))

def generate_customer_base(num_customers=1000):
    customers = []
    for i in range(num_customers):
        segment = random.choices(list(customer_segments.keys()), 
                                 weights=[seg['frequency'] for seg in customer_segments.values()])[0]
        customers.append({
            'Customer ID': f'C{i+1}',
            'Customer Name': f'Customer {i+1}',
            'Segment': segment,
            'Loyalty Score': random.randint(1, 100)
        })
    return pd.DataFrame(customers)

def simulate_marketing_campaign(date, products_df):
    if random.random() < 0.1:  # 10% chance of a marketing campaign on any given day
        eligible_products = products_df[products_df['Promotion Fatigue'] < 3]
        if not eligible_products.empty:
            campaign_product = eligible_products.sample().iloc[0]
            campaign_boost = random.uniform(1.1, 1.5)  # 10-50% boost
            
            # Update promotion fatigue
            products_df.loc[products_df['Product ID'] == campaign_product['Product ID'], 'Promotion Fatigue'] += 1
            products_df.loc[products_df['Product ID'] == campaign_product['Product ID'], 'Last Promotion Date'] = date
            
            return campaign_product['Product ID'], campaign_boost
    return None, 1

def generate_synthetic_data():
    products_df = generate_products(product_hierarchy)
    customers_df = generate_customer_base()
    
    data = []
    stock_levels = {product: random.randint(50, 200) for product in products_df['Product ID']}
    
    for date in date_range:
        products_df = products_df.apply(lambda x: update_product_lifecycle(x, date), axis=1)
        
        # Reset promotion fatigue for products not promoted in the last 30 days

        '''
        products_df.loc[
            (products_df['Last Promotion Date'].notna()) & 
            ((date - products_df['Last Promotion Date']).dt.days > 30), 
            'Promotion Fatigue'
        ] = 0
        '''
        products_df['Last Promotion Date'] = pd.to_datetime(products_df['Last Promotion Date']) #This line converts the 'Last Promotion Date' column to datetime objects
        products_df.loc[
          (products_df['Last Promotion Date'].notna()) & 
          ((date - products_df['Last Promotion Date']).dt.days > 30), 
           'Promotion Fatigue'
        ] = 0
        campaign_product, campaign_boost = simulate_marketing_campaign(date, products_df)
        
        # Introduce new products
        '''
        if random.random() < 0.01:  # 1% chance of new product introduction each day
            new_product = generate_products(product_hierarchy).iloc[0]
            #products_df = products_df.append(new_product, ignore_index=True)
            products_df = pd.concat([products_df, pd.DataFrame([new_product])], ignore_index=True) #This line uses the concat method to add the new_product to the products_df DataFrame
            new_product['Launch Date'] = date
            products_df = products_df.append(new_product, ignore_index=True)
            stock_levels[new_product['Product ID']] = random.randint(50, 200)
        '''
        # Introduce new products
        if random.random() < 0.01:  # 1% chance of new product introduction each day
            new_product = generate_products(product_hierarchy).iloc[0]
            #products_df = products_df.append(new_product, ignore_index=True)
            products_df = pd.concat([products_df, pd.DataFrame([new_product])], ignore_index=True) #This line uses the concat method to add the new_product to the products_df DataFrame
            new_product['Launch Date'] = date
            #products_df = products_df.append(new_product, ignore_index=True) # This line was causing the error. It's redundant since the new product was already added in the line above
            stock_levels[new_product['Product ID']] = random.randint(50, 200)

        for _ in range(random.randint(50, 200)):  # Simulate 50-200 transactions per day
            customer = customers_df.sample().iloc[0]
            cart_products = []
            
            for _ in range(random.randint(1, 5)):  # Simulate 1-5 products per transaction
                product = products_df.sample().iloc[0]
                
                if stock_levels[product['Product ID']] <= 0:
                    continue  # Skip if product is out of stock
                
                base_price = calculate_price(product, date, economic_indicators)
                
                # Apply marketing campaign boost if applicable
                price_multiplier = campaign_boost if product['Product ID'] == campaign_product else 1
                
                # Apply loyalty discount
                loyalty_discount = min(customer['Loyalty Score'] * 0.001, 0.1)  # Max 10% discount
                
                final_price = base_price * price_multiplier * (1 - loyalty_discount)
                
                # Calculate quantity based on price sensitivity and cross-product effects
                base_quantity = random.randint(1, 5)
                price_ratio = final_price / product['Base Price']
                quantity = calculate_quantity(base_quantity, price_ratio, product['Price Sensitivity'])
                quantity = adjust_quantity_for_related_products(quantity, product, cart_products)
                
                revenue = final_price * quantity
                cost = product['Base Price'] * 0.6 * quantity  # Assume 60% of base price is cost
                profit = revenue - cost
                
                stock_levels[product['Product ID']] -= quantity
                
                data.append({
                    'Transaction ID': f'T{len(data) + 1}',
                    'Order Date': date,
                    'Ship Date': date + timedelta(days=random.randint(1, 7)),
                    'Ship Mode': random.choice(['Standard Class', 'Second Class', 'First Class', 'Same Day']),
                    'Customer ID': customer['Customer ID'],
                    'Customer Name': customer['Customer Name'],
                    'Segment': customer['Segment'],
                    'City': random.choices(list(cities.keys()), weights=list(cities.values()))[0],
                    'Product ID': product['Product ID'],
                    'Category': product['Category'],
                    'Subcategory': product['Subcategory'],
                    'Product Type': product['Product Type'],
                    'Product Name': product['Product Name'],
                    'Sales': revenue,
                    'Quantity': quantity,
                    'Unit Price': final_price,
                    'Discount': loyalty_discount,
                    'Profit': profit,
                    'Stock Level': stock_levels[product['Product ID']],
                    'Price Sensitivity': product['Price Sensitivity'],
                    'Lifecycle Stage': product['Lifecycle Stage'],
                    'Promotion Fatigue': product['Promotion Fatigue'],
                    'Season': get_season(date)
                })
                
                cart_products.append(product)
        
        # Restock products
        for product_id, stock in stock_levels.items():
            if stock < 20:  # Restock when inventory is low
                stock_levels[product_id] += random.randint(50, 100)
    
    return pd.DataFrame(data)

# Generate and save the data
df = generate_synthetic_data()
#df.to_csv('advanced_consumer_behavior_superstore_data.csv', index=False)
print("Advanced synthetic dataset with enhanced consumer behavior created and saved as 'advanced_consumer_behavior_superstore_data.csv'.")
