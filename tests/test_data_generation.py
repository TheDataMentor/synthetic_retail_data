import unittest
import pandas as pd
from src.data_generation import generate_synthetic_data

class TestDataGeneration(unittest.TestCase):
    def setUp(self):
        self.df = generate_synthetic_data()

    def test_dataframe_not_empty(self):
        self.assertFalse(self.df.empty)

    def test_expected_columns_present(self):
        expected_columns = ['Transaction ID', 'Order Date', 'Customer ID', 'Product ID', 'Category', 'Sales', 'Quantity']
        for column in expected_columns:
            self.assertIn(column, self.df.columns)

    def test_sales_always_positive(self):
        self.assertTrue((self.df['Sales'] >= 0).all())

    def test_quantity_always_positive_integer(self):
        self.assertTrue((self.df['Quantity'] > 0).all())
        self.assertTrue(self.df['Quantity'].dtype in ['int64', 'int32'])

if __name__ == '__main__':
    unittest.main()
