import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime, date
import logging

logging.basicConfig(level=logging.INFO)

# Logo in upper right
logo_path = Path("static/TTU_LOGO.jpg")
if logo_path.exists():
    col1, col2 = st.columns([6, 1])
    with col2:
        st.image(str(logo_path), width=120)

st.title("Business Data Entry Portal")
st.markdown("""
Enter new business data through secure forms. These forms connect directly to your operational database and support real business workflows.
""")

# Database connection helper
def get_db_connection():
    return sqlite3.connect("graphite_analytics.db")

# Get customers and products for dropdowns
def load_reference_data():
    try:
        with get_db_connection() as conn:
            customers_df = pd.read_sql("SELECT CustomerID, CustomerName FROM Customers ORDER BY CustomerName", conn)
            products_df = pd.read_sql("SELECT ProductID, ProductName FROM Products ORDER BY ProductName", conn)
            return customers_df, products_df
    except Exception as e:
        logging.error(f"Failed to load reference data: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Tab layout for different forms
tab1, tab2, tab3 = st.tabs(["New Customer Order", "Product Management", "Customer Information"])

with tab1:
    st.subheader("Create New Customer Order")
    
    with st.form("new_order_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            order_id = st.text_input("Order ID", placeholder="Enter unique order ID")
            customer_id = st.text_input("Customer ID", placeholder="Customer code (e.g., ACMECORP)")
            customer_name = st.text_input("Customer Name", placeholder="Full company name")
            order_date = st.date_input("Order Date", value=datetime.now().date())
        
        with col2:
            customer_po = st.text_input("Customer PO Number", placeholder="Customer's purchase order")
            delivery_date = st.date_input("Requested Delivery Date")
            salesperson = st.selectbox("Salesperson", 
                                     ["John Smith", "Lisa Johnson", "Robert Chen", "Maria Garcia", "David Wilson"])
            order_status = st.selectbox("Order Status", ["Open", "Processing", "On Hold", "Shipped"])
        
        st.subheader("Order Items")
        
        # Product line items
        product_id = st.text_input("Product ID", placeholder="Enter product code")
        product_name = st.text_input("Product Description", placeholder="Product description")
        quantity = st.number_input("Quantity", min_value=1, value=1)
        unit_price = st.number_input("Unit Price ($)", min_value=0.01, value=100.00, format="%.2f")
        total_cost = quantity * unit_price
        st.write(f"**Line Total: ${total_cost:,.2f}**")
        
        special_instructions = st.text_area("Special Instructions", 
                                          placeholder="Any special requirements or notes...")
        
        submitted_order = st.form_submit_button("Submit Order", type="primary")
        
        if submitted_order:
            if order_id and customer_id and customer_name and product_id:
                try:
                    with get_db_connection() as conn:
                        cursor = conn.cursor()
                        
                        # Insert customer if not exists
                        cursor.execute("""
                        INSERT OR REPLACE INTO Customers 
                        (CustomerID, CustomerName, ContactPerson, Email, Phone)
                        VALUES (?, ?, ?, ?, ?)
                        """, (customer_id, customer_name, "Contact Person", 
                             f"{customer_id.lower()}@company.com", "555-0100"))
                        
                        # Insert product if not exists
                        cursor.execute("""
                        INSERT OR REPLACE INTO Products 
                        (ProductID, ProductName, Description, Category, UnitPrice)
                        VALUES (?, ?, ?, ?, ?)
                        """, (product_id, product_name, product_name, "Custom", unit_price))
                        
                        # Insert order
                        cursor.execute("""
                        INSERT INTO Orders 
                        (OrderID, CustomerID, OrderDate, DeliveryDate, Status, TotalAmount, CustomerPO)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (order_id, customer_id, order_date.isoformat(), 
                             delivery_date.isoformat(), order_status, total_cost, customer_po))
                        
                        # Insert order detail
                        cursor.execute("""
                        INSERT INTO OrderDetails 
                        (OrderID, ProductID, Quantity, UnitPrice, TotalCost)
                        VALUES (?, ?, ?, ?, ?)
                        """, (order_id, product_id, quantity, unit_price, total_cost))
                        
                        conn.commit()
                        st.success(f"✅ Order {order_id} created successfully!")
                        st.balloons()
                        
                except Exception as e:
                    st.error(f"Failed to create order: {str(e)}")
                    logging.error(f"Order creation failed: {e}")
            else:
                st.error("Please fill in all required fields")

with tab2:
    st.subheader("Product Management")
    
    with st.form("product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_product_id = st.text_input("Product ID", placeholder="Unique product code")
            new_product_name = st.text_input("Product Name", placeholder="Product display name")
            product_category = st.selectbox("Category", 
                                          ["Graphite Components", "Carbon Parts", "Specialized Fixtures", 
                                           "Heat Shields", "Conductive Elements", "Custom Manufacturing"])
        
        with col2:
            new_unit_price = st.number_input("Standard Unit Price ($)", min_value=0.01, value=500.00, format="%.2f")
            product_weight = st.number_input("Weight (lbs)", min_value=0.01, value=1.0, format="%.2f")
            lead_time_days = st.number_input("Standard Lead Time (days)", min_value=1, value=30)
        
        product_description = st.text_area("Product Description", 
                                         placeholder="Detailed product specifications and applications...")
        
        submitted_product = st.form_submit_button("Add Product", type="primary")
        
        if submitted_product:
            if new_product_id and new_product_name:
                try:
                    with get_db_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                        INSERT OR REPLACE INTO Products 
                        (ProductID, ProductName, Description, Category, UnitPrice)
                        VALUES (?, ?, ?, ?, ?)
                        """, (new_product_id, new_product_name, product_description, 
                             product_category, new_unit_price))
                        conn.commit()
                        st.success(f"✅ Product {new_product_id} added successfully!")
                        
                except Exception as e:
                    st.error(f"Failed to add product: {str(e)}")
                    logging.error(f"Product creation failed: {e}")
            else:
                st.error("Please fill in Product ID and Name")

with tab3:
    st.subheader("Customer Information Management")
    
    with st.form("customer_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_customer_id = st.text_input("Customer ID", placeholder="Unique customer code")
            new_customer_name = st.text_input("Company Name", placeholder="Full legal company name")
            contact_person = st.text_input("Primary Contact", placeholder="Contact person name")
            contact_email = st.text_input("Email", placeholder="contact@company.com")
        
        with col2:
            contact_phone = st.text_input("Phone", placeholder="555-123-4567")
            billing_address = st.text_area("Billing Address", placeholder="Street address, City, State, ZIP")
            shipping_address = st.text_area("Shipping Address", placeholder="Street address, City, State, ZIP")
            payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 60", "Net 90", "COD", "Prepaid"])
        
        customer_notes = st.text_area("Customer Notes", 
                                    placeholder="Special requirements, preferences, or important notes...")
        
        submitted_customer = st.form_submit_button("Add/Update Customer", type="primary")
        
        if submitted_customer:
            if new_customer_id and new_customer_name:
                try:
                    with get_db_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                        INSERT OR REPLACE INTO Customers 
                        (CustomerID, CustomerName, ContactPerson, Email, Phone)
                        VALUES (?, ?, ?, ?, ?)
                        """, (new_customer_id, new_customer_name, contact_person, 
                             contact_email, contact_phone))
                        conn.commit()
                        st.success(f"✅ Customer {new_customer_id} saved successfully!")
                        
                except Exception as e:
                    st.error(f"Failed to save customer: {str(e)}")
                    logging.error(f"Customer creation failed: {e}")
            else:
                st.error("Please fill in Customer ID and Company Name")

# Recent activity section
st.subheader("Recent Form Submissions")
try:
    with get_db_connection() as conn:
        recent_orders = pd.read_sql("""
        SELECT o.OrderID, o.CustomerID, c.CustomerName, o.OrderDate, o.TotalAmount
        FROM Orders o
        JOIN Customers c ON o.CustomerID = c.CustomerID
        ORDER BY o.OrderDate DESC
        LIMIT 5
        """, conn)
        
        if not recent_orders.empty:
            st.dataframe(recent_orders, use_container_width=True)
        else:
            st.info("No recent orders to display.")
            
except Exception as e:
    st.error("Unable to load recent activity")
    logging.error(f"Failed to load recent orders: {e}")
