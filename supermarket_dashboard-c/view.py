#Business logic
"""
VIEW LAYER - Business Logic
This file processes data for visualization:
- Calculations
- Grouping
- Aggregations
"""

import numpy as np

class SupermarketView:
    """
    This class is like a DATA ANALYST
    It analyzes data and prepares it for display 
    """
    
    def __init__(self, model):
        """Connect to the model (data source)"""
        self.model = model
    
    def get_sales_by_branch(self):
        """
        Calculate total sales for each branch
        Returns: branch names and their sales
        """
        branches = self.model.get_unique_values('Branch')
        sales = []
        
        for branch in branches:
            # Filter data for this branch
            branch_data = self.model.filter_by_value('Branch', branch)
            # Sum all sales for this branch
            total = np.sum(branch_data['Total'])
            sales.append(total)
        
        return branches, np.array(sales)
    
    def get_sales_by_city(self):
        """Calculate total sales for each city"""
        cities = self.model.get_unique_values('City')
        sales = []
        
        for city in cities:
            city_data = self.model.filter_by_value('City', city)
            total = np.sum(city_data['Total'])
            sales.append(total)
        
        return cities, np.array(sales)
    
    def get_sales_by_product_line(self):
        """Calculate sales for each product category"""
        products = self.model.get_unique_values('Product line')
        sales = []
        
        for product in products:
            product_data = self.model.filter_by_value('Product line', product)
            total = np.sum(product_data['Total'])
            sales.append(total)
        
        return products, np.array(sales)
    
    def get_payment_method_distribution(self):
        """Count how many times each payment method was used"""
        methods = self.model.get_unique_values('Payment')
        counts = []
        
        for method in methods:
            method_data = self.model.filter_by_value('Payment', method)
            count = len(method_data['Payment'])
            counts.append(count)
        
        return methods, np.array(counts)
    
    def get_customer_type_analysis(self):
        """Compare Member vs Normal customers"""
        customer_types = self.model.get_unique_values('Customer type')
        sales = []
        counts = []
        
        for ctype in customer_types:
            ctype_data = self.model.filter_by_value('Customer type', ctype)
            sales.append(np.sum(ctype_data['Total']))
            counts.append(len(ctype_data['Total']))
        
        return customer_types, np.array(sales), np.array(counts)
    
    def get_gender_analysis(self):
        """Compare Male vs Female purchases"""
        genders = self.model.get_unique_values('Gender')
        sales = []
        counts = []
        
        for gender in genders:
            gender_data = self.model.filter_by_value('Gender', gender)
            sales.append(np.sum(gender_data['Total']))
            counts.append(len(gender_data['Total']))
        
        return genders, np.array(sales), np.array(counts)
    
    def get_rating_distribution(self):
        """
        Create rating histogram
        Shows how many transactions got each rating (4.0, 5.0, etc.)
        """
        ratings = self.model.get_column('Rating')
        
        # Create bins for ratings (4.0-4.5, 4.5-5.0, etc.)
        bins = np.arange(4.0, 10.5, 0.5)
        
        # Count how many ratings fall in each bin
        hist, bin_edges = np.histogram(ratings, bins=bins)
        
        return bin_edges, hist
    
    def get_monthly_sales_trend(self):
        """
        Calculate sales for each month
        This shows business trend over time
        """
        dates = self.model.get_column('Date')
        totals = self.model.get_column('Total')
        
        # Dictionary to store: month -> total sales
        monthly_sales = {}
        
        for i, date in enumerate(dates):
            # Extract month from date (format: 1/5/2019 -> month is 1)
            try:
                month = date.split('/')[0]
                if month not in monthly_sales:
                    monthly_sales[month] = 0
                monthly_sales[month] += totals[i]
            except:
                continue
        
        # Sort by month number
        months = sorted(monthly_sales.keys(), key=lambda x: int(x))
        sales = [monthly_sales[m] for m in months]
        
        # Convert month numbers to names
        month_names = []
        month_map = {
            '1': 'January', '2': 'February', '3': 'March',
            '4': 'April', '5': 'May', '6': 'June',
            '7': 'July', '8': 'August', '9': 'September',
            '10': 'October', '11': 'November', '12': 'December'
        }
        
        for m in months:
            month_names.append(month_map.get(m, m))
        
        return month_names, np.array(sales)
    
    def get_top_products(self, top_n=5):
        """Get top N selling products"""
        products, sales = self.get_sales_by_product_line()
        
        # Sort by sales (descending)
        sorted_indices = np.argsort(sales)[::-1]
        
        # Get top N
        top_products = products[sorted_indices[:top_n]]
        top_sales = sales[sorted_indices[:top_n]]
        
        return top_products, top_sales
    
    def get_average_basket_size(self):
        """
        Calculate average quantity per transaction
        Shows how many items customers buy on average
        """
        quantities = self.model.get_column('Quantity')
        return np.mean(quantities)
    
    def get_average_transaction_value(self):
        """Average amount spent per transaction"""
        totals = self.model.get_column('Total')
        return np.mean(totals)
    
    def get_kpis(self):
        """
        KPI = Key Performance Indicator
        Important metrics for business dashboard
        """
        totals = self.model.get_column('Total')
        quantities = self.model.get_column('Quantity')
        ratings = self.model.get_column('Rating')
        
        return {
            'total_revenue': np.sum(totals),
            'total_transactions': len(totals),
            'average_transaction': np.mean(totals),
            'total_items_sold': np.sum(quantities),
            'average_rating': np.mean(ratings),
            'max_transaction': np.max(totals),
            'min_transaction': np.min(totals)
        }