import unittest
import pdb
from item7680 import *

# Verify Related Behaviors in TestCase Subclasses
# Consider Interactive Debugging with pdb
class TestDataLoading(unittest.TestCase):
    def setUp(self):
        """Sets up the path for sample data CSV file."""
        self.filepath = 'sample_data.csv'

    def test_load_data(self):
        """Test that load_data loads data without enforcing specific data types."""
        df = load_data(self.filepath)
        
        if df['age'].dtype != 'int64':
            breakpoint()
            self.fail("Expected 'age' column to be int64, but got float64")
        
        if df['height'].dtype != 'float64':
            breakpoint()
            self.fail("Expected 'height' column to be float64")
        
        if df['weight'].dtype != 'int64':
            breakpoint()
            self.fail("Expected 'weight' column to be int64, but got float64")

    def test_clean_data(self):
        """Test that clean_data ensures correct data types."""
        df = load_data(self.filepath)
        df_cleaned = clean_data(df)
        
        self.assertEqual(df_cleaned['age'].dtype, 'int64')
        self.assertEqual(df_cleaned['height'].dtype, 'float64')
        self.assertEqual(df_cleaned['weight'].dtype, 'int64')

if __name__ == "__main__":
    unittest.main()
