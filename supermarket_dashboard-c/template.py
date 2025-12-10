#Streamlit UI
"""
TEMPLATE LAYER - User Interface
This file creates the dashboard that users see:
- Layout
- Charts
- Interactions
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

class DashboardTemplate:
    """
    This class is like a DESIGNER
    It creates the visual dashboard
    """
    
    def __init__(self, view):
        """Connect to the view (business logic)"""
        self.view = view
    
    def render(self):
        """
        Main function to display the dashboard
        This is what users see when they open the app
        """
        # Page title
        st.title("🛒 Supermarket Sales Dashboard")
        st.markdown("### Real-time insights from your retail data")
        st.markdown("---")
        
        # Show KPIs at the top
        self._render_kpis()
        
        st.markdown("---")
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Sales Analysis", 
            "👥 Customer Insights",
            "📈 Trends",
            "⭐ Ratings"
        ])
        
        with tab1:
            self._render_sales_analysis()
        
        with tab2:
            self._render_customer_insights()
        
        with tab3:
            self._render_trends()
        
        with tab4:
            self._render_ratings()
    
    def _render_kpis(self):
        """
        Display Key Performance Indicators
        These are the most important numbers at a glance
        """
        kpis = self.view.get_kpis()
        
        # Create 4 columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Total Revenue",
                value=f"${kpis['total_revenue']:,.2f}"
            )
        
        with col2:
            st.metric(
                label="🛍️ Total Transactions",
                value=f"{kpis['total_transactions']:,}"
            )
        
        with col3:
            st.metric(
                label="📦 Items Sold",
                value=f"{int(kpis['total_items_sold']):,}"
            )
        
        with col4:
            st.metric(
                label="⭐ Avg Rating",
                value=f"{kpis['average_rating']:.1f}/10"
            )
    
    def _render_sales_analysis(self):
        """Show sales breakdown by branch, city, and product"""
        st.subheader("Sales Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales by Branch
            st.markdown("#### Sales by Branch")
            branches, sales = self.view.get_sales_by_branch()
            fig, ax = plt.subplots(figsize=(6, 4))
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            ax.bar(branches, sales, color=colors)
            ax.set_ylabel('Total Sales ($)')
            ax.set_title('Branch Performance')
            # Add value labels on bars
            for i, v in enumerate(sales):
                ax.text(i, v, f'${v:,.0f}', ha='center', va='bottom')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            # Sales by City
            st.markdown("#### Sales by City")
            cities, sales = self.view.get_sales_by_city()
            fig, ax = plt.subplots(figsize=(6, 4))
            colors = ['#95E1D3', '#F38181', '#FCE77D']
            ax.bar(cities, sales, color=colors)
            ax.set_ylabel('Total Sales ($)')
            ax.set_title('City Performance')
            plt.xticks(rotation=15)
            for i, v in enumerate(sales):
                ax.text(i, v, f'${v:,.0f}', ha='center', va='bottom')
            plt.tight_layout()
            st.pyplot(fig)
        
        st.markdown("---")
        
        # Top Products
        st.markdown("#### Top 5 Product Lines")
        products, sales = self.view.get_top_products(top_n=5)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = plt.cm.Spectral(np.linspace(0.2, 0.8, len(products)))
        bars = ax.barh(products, sales, color=colors)
        ax.set_xlabel('Total Sales ($)')
        ax.set_title('Best Selling Product Categories')
        
        # Add value labels
        for i, v in enumerate(sales):
            ax.text(v, i, f'  ${v:,.0f}', va='center')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def _render_customer_insights(self):
        """Show customer behavior analysis"""
        st.subheader("Customer Behavior")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer Type
            st.markdown("#### Member vs Normal Customers")
            ctypes, sales, counts = self.view.get_customer_type_analysis()
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            
            # Sales comparison
            colors = ['#6C5CE7', '#00B894']
            ax1.pie(sales, labels=ctypes, autopct='%1.1f%%', 
                    startangle=90, colors=colors)
            ax1.set_title('Sales by Customer Type')
            
            # Transaction count
            ax2.bar(ctypes, counts, color=colors)
            ax2.set_ylabel('Number of Transactions')
            ax2.set_title('Transaction Count')
            for i, v in enumerate(counts):
                ax2.text(i, v, str(v), ha='center', va='bottom')
            
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            # Gender Analysis
            st.markdown("#### Gender Distribution")
            genders, sales, counts = self.view.get_gender_analysis()
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            
            # Sales by gender
            colors = ['#A29BFE', '#FD79A8']
            ax1.pie(sales, labels=genders, autopct='%1.1f%%',
                    startangle=90, colors=colors)
            ax1.set_title('Sales by Gender')
            
            # Count by gender
            ax2.bar(genders, counts, color=colors)
            ax2.set_ylabel('Number of Purchases')
            ax2.set_title('Purchase Count')
            for i, v in enumerate(counts):
                ax2.text(i, v, str(v), ha='center', va='bottom')
            
            plt.tight_layout()
            st.pyplot(fig)
        
        st.markdown("---")
        
        # Payment Methods
        st.markdown("#### Payment Method Preferences")
        methods, counts = self.view.get_payment_method_distribution()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#74B9FF', '#A29BFE', '#FD79A8']
        wedges, texts, autotexts = ax.pie(
            counts, 
            labels=methods, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=[0.05] * len(methods)
        )
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        ax.set_title('Payment Method Distribution', fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    def _render_trends(self):
        """Show sales trends over time"""
        st.subheader("Sales Trends")
        
        months, sales = self.view.get_monthly_sales_trend()
        
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(months, sales, marker='o', linewidth=2, 
                markersize=8, color='#6C5CE7')
        ax.fill_between(range(len(months)), sales, alpha=0.3, color='#6C5CE7')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Total Sales ($)', fontsize=12)
        ax.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Add value labels
        for i, v in enumerate(sales):
            ax.text(i, v, f'${v:,.0f}', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Additional metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_basket = self.view.get_average_basket_size()
            st.metric("🛒 Avg Items per Transaction", f"{avg_basket:.1f}")
        
        with col2:
            avg_transaction = self.view.get_average_transaction_value()
            st.metric("💵 Avg Transaction Value", f"${avg_transaction:.2f}")
        
        with col3:
            kpis = self.view.get_kpis()
            st.metric("📊 Highest Sale", f"${kpis['max_transaction']:.2f}")
    
    def _render_ratings(self):
        """Show customer satisfaction ratings"""
        st.subheader("Customer Satisfaction")
        
        bin_edges, hist = self.view.get_rating_distribution()
        
        # Create rating ranges for x-axis
        rating_ranges = []
        for i in range(len(bin_edges)-1):
            rating_ranges.append(f"{bin_edges[i]:.1f}-{bin_edges[i+1]:.1f}")
        
        fig, ax = plt.subplots(figsize=(12, 5))
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(hist)))
        bars = ax.bar(rating_ranges, hist, color=colors, edgecolor='black')
        
        ax.set_xlabel('Rating Range', fontsize=12)
        ax.set_ylabel('Number of Transactions', fontsize=12)
        ax.set_title('Customer Rating Distribution', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Rating summary
        kpis = self.view.get_kpis()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⭐ Average Rating", f"{kpis['average_rating']:.2f}/10")
        
        with col2:
            # Calculate percentage of high ratings (>7)
            ratings = self.view.view.model.get_column('Rating')
            high_ratings = np.sum(ratings > 7)
            pct = (high_ratings / len(ratings)) * 100
            st.metric("👍 High Ratings (>7)", f"{pct:.1f}%")
        
        with col3:
            st.metric("📊 Total Ratings", f"{len(ratings):,}")