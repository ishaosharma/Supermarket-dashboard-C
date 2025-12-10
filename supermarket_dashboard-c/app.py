#Main application
"""
MAIN APPLICATION FILE
This connects all layers together and runs the dashboard
"""

import streamlit as st
from model import SupermarketModel
from view import SupermarketView
from template import DashboardTemplate

def main():
    """
    Main function - Entry point of the application
    This is what runs when you start the app
    """
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="Supermarket Dashboard",
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        h1 {
            color: #2C3E50;
        }
        .stMetric {
            background-color: #F8F9FA;
            padding: 10px;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar for file upload and info
    with st.sidebar:
        st.header("📂 Data Source")
        st.info("Upload your supermarket sales CSV file")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file", 
            type=['csv'],
            help="Upload your supermarket_sales.csv file"
        )
        
        st.markdown("---")
        st.markdown("### 📊 About This Dashboard")
        st.markdown("""
        This dashboard analyzes:
        - 💰 Sales performance
        - 🏢 Branch comparison
        - 👥 Customer behavior
        - 📈 Sales trends
        - ⭐ Customer satisfaction
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 Built With")
        st.markdown("""
        - **NumPy** - Data processing
        - **Matplotlib** - Visualizations
        - **Streamlit** - Web interface
        """)
    
    # Main content area
    if uploaded_file is not None: 
        # Save uploaded file temporarily
        with open("temp_data.csv", "wb") as f: 
            f.write(uploaded_file.getbuffer())
        
        # Show loading spinner
        with st.spinner("🔄 Loading and processing data..."):
            try:
                # STEP 1: Initialize Model (Data Layer)
                model = SupermarketModel()
                
                # STEP 2: Load and Clean Data
                success = model.load_csv("temp_data.csv")
                
                if success:
                    # Display data summary
                    summary = model.get_summary()
                    
                    with st.sidebar:
                        st.success("✅ Data loaded successfully!")
                        st.markdown("### 📋 Data Summary")
                        st.write(f"Total Records: **{summary['total_rows']:,}**")
                        st.write(f"Total Sales: **${summary['total_sales']:,.2f}**")
                        st.write(f"Branches: **{summary['branches']}**")
                        st.write(f"Cities: **{summary['cities']}**")
                        st.write(f"Product Lines: **{summary['product_lines']}**")
                    
                    # STEP 3: Initialize View (Business Logic Layer)
                    view = SupermarketView(model)
                    
                    # STEP 4: Initialize Template (UI Layer)
                    template = DashboardTemplate(view)
                    
                    # STEP 5: Render Dashboard
                    template.render()
                    
                else:
                    st.error("❌ Failed to load data. Please check your CSV file.")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Please make sure your CSV file has the correct format.")
    
    else:
        # Welcome screen when no file is uploaded
        st.markdown("""
        ## 👋 Welcome to Supermarket Sales Dashboard!
        
        ### 🚀 Getting Started:
        1. Click on **"Browse files"** in the sidebar
        2. Upload your `supermarket_sales.csv` file
        3. Explore the interactive dashboard!
        
        ### 📊 What You'll See:
        - **Key Metrics**: Total revenue, transactions, and ratings
        - **Sales Analysis**: Performance by branch, city, and products
        - **Customer Insights**: Behavior patterns and preferences
        - **Trends**: Monthly sales patterns
        - **Ratings**: Customer satisfaction analysis
        
        ### 📝 Features:
        ✅ Automatic data cleaning and validation  
        ✅ Real-time calculations using NumPy  
        ✅ Beautiful visualizations with Matplotlib  
        ✅ Interactive filters and tabs  
        
        ---
        
        **Ready to analyze your data?** 👉 Upload your CSV file to begin!
        """)
        
        # Show sample data info
        with st.expander("ℹ️ Expected CSV Format"):
            st.code("""
Required columns:
- Invoice ID
- Branch (A, B, C)
- City
- Customer type (Member, Normal)
- Gender (Male, Female)
- Product line
- Unit price
- Quantity
- Total
- Date
- Payment (Cash, Credit card, Ewallet)
- Rating
            """)

if __name__ == "__main__":
    main()