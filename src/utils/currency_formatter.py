"""
Currency formatting utilities for the GraphiteVision Analytics application.
Provides consistent dollar formatting across all pages.
"""

import pandas as pd
import numpy as np

def format_currency(value):
    """
    Format a single value as currency with $ sign and 2 decimal places.
    
    Args:
        value: Numeric value to format
        
    Returns:
        Formatted string like $1,234.56
    """
    if pd.isna(value) or value is None:
        return "$0.00"
    
    try:
        # Convert to float and format
        numeric_value = float(value)
        return f"${numeric_value:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def format_currency_column(df, column_name):
    """
    Format an entire DataFrame column as currency.
    
    Args:
        df: pandas DataFrame
        column_name: Name of the column to format
        
    Returns:
        DataFrame with formatted currency column
    """
    if column_name in df.columns:
        df[column_name] = df[column_name].apply(format_currency)
    return df

def format_multiple_currency_columns(df, column_names):
    """
    Format multiple DataFrame columns as currency.
    
    Args:
        df: pandas DataFrame
        column_names: List of column names to format
        
    Returns:
        DataFrame with formatted currency columns
    """
    df_copy = df.copy()
    for column_name in column_names:
        if column_name in df_copy.columns:
            df_copy[column_name] = df_copy[column_name].apply(format_currency)
    return df_copy

def get_currency_columns():
    """
    Return list of common currency column names used in the application.
    """
    return [
        'UnitPrice', 'TotalCost', 'TotalRevenue', 'AveragePrice', 
        'TotalOrderValue', 'TotalValue', 'Price', 'Cost', 'Revenue',
        'Amount', 'Total', 'Unitprice', 'AvgPrice', 'TotalAmount'
    ]

# Streamlit display formatting
def display_currency_dataframe(df, currency_columns=None):
    """
    Display a DataFrame in Streamlit with proper currency formatting.
    
    Args:
        df: pandas DataFrame to display
        currency_columns: List of columns to format as currency (auto-detect if None)
        
    Returns:
        DataFrame ready for Streamlit display
    """
    if df.empty:
        return df
    
    if currency_columns is None:
        # Auto-detect currency columns
        currency_columns = [col for col in df.columns if any(
            currency_term.lower() in col.lower() 
            for currency_term in get_currency_columns()
        )]
    
    return format_multiple_currency_columns(df, currency_columns)

if __name__ == "__main__":
    # Test the formatter
    test_data = {
        'Product': ['Item A', 'Item B'],
        'UnitPrice': [1234.567, 9876.54321],
        'TotalRevenue': [12345.67890, 98765.4321]
    }
    test_df = pd.DataFrame(test_data)
    
    print("Original DataFrame:")
    print(test_df)
    
    formatted_df = display_currency_dataframe(test_df)
    print("\nFormatted DataFrame:")
    print(formatted_df)