#Data Handling
"""
MODEL LAYER - Data Handling
This file handles all data operations:
- Loading CSV file
- Cleaning data (removing nulls)
- Converting data types
"""

import numpy as np

class SupermarketModel:
    """
    This class is like a DATA MANAGER
    It loads and cleans your supermarket data
    """
    
    def __init__(self):
        """Initialize empty data storage"""
        self.data = {}
        self.headers = []
        self.row_count = 0
        
    def load_csv(self, filepath):
        """
        Load CSV file and convert to Numpy arrays
        
        How it works:
        1. Read file line by line
        2. Split by comma
        3. Store in arrays
        """
        try:
            # Read the file
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # First line is headers (column names)
            self.headers = lines[0].strip().split(',')
            
            # Initialize dictionary to store each column
            for header in self.headers:
                self.data[header] = []
            
            # Read data rows (skip header)
            for line in lines[1:]:
                values = line.strip().split(',')
                
                # Store each value in its column
                for i, header in enumerate(self.headers):
                    if i < len(values):
                        self.data[header].append(values[i])
                    else:
                        self.data[header].append('')  # Empty if missing
            
            self.row_count = len(lines) - 1
            print(f"✅ Loaded {self.row_count} rows successfully!")
            
            # Convert to numpy arrays
            self._convert_to_numpy()
            
            # Clean the data
            self._clean_data()
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return False
    
    def _convert_to_numpy(self):
        """
        Convert lists to Numpy arrays
        Numpy arrays are faster and better for calculations
        """
        for header in self.headers:
            self.data[header] = np.array(self.data[header])
    
    def _clean_data(self):
        """
        Clean the data:
        1. Remove rows with missing important data
        2. Convert numbers from text to actual numbers
        """
        print("\n🧹 Cleaning data...")
        
        # Check for null values in important columns
        important_columns = ['Total', 'Quantity', 'Rating', 'Branch']
        
        # Find rows where important data is missing
        valid_rows = np.ones(self.row_count, dtype=bool)  # Start with all True
        
        for col in important_columns:
            if col in self.data:
                # Mark rows as invalid if empty
                valid_rows = valid_rows & (self.data[col] != '')
        
        # Count removed rows
        removed = self.row_count - np.sum(valid_rows)
        
        if removed > 0:
            print(f"⚠️ Removed {removed} rows with missing data")
            # Keep only valid rows
            for header in self.headers:
                self.data[header] = self.data[header][valid_rows]
            self.row_count = np.sum(valid_rows)
        else:
            print("✅ No missing data found!")
        
        # Convert numeric columns from text to numbers
        numeric_columns = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 
                          'cogs', 'gross margin percentage', 'gross income', 'Rating']
        
        for col in numeric_columns:
            if col in self.data:
                # Convert to float (decimal numbers)
                self.data[col] = self._safe_convert_to_float(self.data[col])
        
        print(f"✅ Final dataset: {self.row_count} clean rows\n")
    
    def _safe_convert_to_float(self, arr):
        """
        Safely convert text numbers to float
        If conversion fails, use 0.0
        """
        result = np.zeros(len(arr), dtype=float)
        for i, val in enumerate(arr):
            try:
                result[i] = float(val)
            except:
                result[i] = 0.0
        return result
    
    def get_column(self, column_name):
        """Get a specific column"""
        return self.data.get(column_name, np.array([]))
    
    def get_unique_values(self, column_name):
        """Get unique values from a column (like unique branches: A, B, C)"""
        return np.unique(self.data.get(column_name, np.array([])))
    
    def filter_by_value(self, column_name, value):
        """
        Filter data by a specific value
        Example: Get all sales from Branch A
        """
        mask = self.data[column_name] == value
        filtered_data = {}
        for header in self.headers:
            filtered_data[header] = self.data[header][mask]
        return filtered_data
    
    def get_summary(self):
        """Get basic statistics about the dataset"""
        return {
            'total_rows': self.row_count,
            'total_sales': np.sum(self.data['Total']),
            'average_rating': np.mean(self.data['Rating']),
            'total_quantity': np.sum(self.data['Quantity']),
            'branches': len(self.get_unique_values('Branch')),
            'cities': len(self.get_unique_values('City')),
            'product_lines': len(self.get_unique_values('Product line'))
        }