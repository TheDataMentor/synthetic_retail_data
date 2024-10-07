import unittest
import pandas as pd
from src.data_analysis import calculate_summary_statistics, identify_top_products

class TestDataAnalysis(unittest.TestCase):
    def setUp(self):
        # Create a sample dataframe for testing
        self.df = pd.DataFrame({
            'Category': ['A', 'B', 'A', 'C', 'B'],
            'Sales': [100, 200, 150, 300, 250],
            'Quantity': [1, 2, 1, 3, 2],
            'Profit': [10, 20, 15, 30, 25],
            'Product ID': ['P1', 'P2', 'P3', 'P4', 'P5']
        })

    def test_calculate_summary_statistics(self):
        summary = calculate_summary_statistics(self.df)
        self.assertEqual(len(summary), 3)  # 3 categories
        self.assertIn(('Sales', 'mean'), summary.columns)

    def test_identify_top_products(self):
        top_products = identify_top_products(self.df, n=3)
        self.assertEqual(len(top_products), 3)
        self.assertEqual(top_products.index[0], 'P4')  # Highest sales

if __name__ == '__main__':
    unittest.main()
