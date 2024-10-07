import matplotlib.pyplot as plt
import seaborn as sns

def plot_sales_trend(df):
    plt.figure(figsize=(12, 6))
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    daily_sales = df.groupby('Order Date')['Sales'].sum()
    daily_sales.plot()
    plt.title('Daily Sales Trend')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.savefig('results/sales_trend.png')
    plt.close()

def plot_category_distribution(df):
    plt.figure(figsize=(10, 6))
    df['Category'].value_counts().plot(kind='bar')
    plt.title('Product Category Distribution')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.savefig('results/product_category_distribution.png')
    plt.close()

# Add more visualization functions as needed
