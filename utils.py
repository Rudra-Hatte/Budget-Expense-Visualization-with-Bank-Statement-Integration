import pandas as pd
import re
import os
from datetime import datetime
import numpy as np

# Dictionary mapping keywords to expense categories
CATEGORY_KEYWORDS = {
    "Groceries": ["market", "grocery", "supermarket", "store", "food mart", "walmart", "target"],
    "Dining": ["restaurant", "cafe", "coffee", "dining", "food", "bakery", "takeout", "doordash", "uber eats"],
    "Transport": ["uber", "lyft", "metro", "bus", "train", "taxi", "fuel", "petrol", "gas", "parking", "toll"],
    "Entertainment": ["cinema", "movie", "netflix", "spotify", "music", "game", "hbo", "disney", "hulu", "ticket"],
    "Utilities": ["electric", "water", "gas", "internet", "utility", "phone", "bill", "subscription", "service"],
    "Shopping": ["amazon", "mall", "shopping", "store", "clothes", "purchase", "online", "retail"],
    "Income": ["salary", "deposit", "refund", "credit", "interest", "payment received", "transfer in"],
    "Rent": ["rent", "lease", "housing", "apartment"],
    "Healthcare": ["doctor", "medical", "pharmacy", "hospital", "clinic", "health", "dental"],
    "Education": ["tuition", "school", "college", "course", "book", "university"],
    "Travel": ["hotel", "flight", "airline", "airbnb", "booking", "travel", "vacation"]
    # Add more categories as needed
}

def load_bank_statement(file_path):
    """
    Load bank statement from CSV or Excel file.
    
    Args:
        file_path (str): Path to the bank statement file
    
    Returns:
        pandas.DataFrame: Processed bank statement
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel files.")
        
        # Standardize column names - adjust these based on your bank statement format
        expected_columns = ['Date', 'Description', 'Amount', 'Type']
        
        # Try to find and rename columns that might match our expected format
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            if any(date_key in col_lower for date_key in ['date', 'time']):
                column_mapping[col] = 'Date'
            elif any(desc_key in col_lower for desc_key in ['desc', 'narration', 'transaction', 'particular']):
                column_mapping[col] = 'Description'
            elif any(amt_key in col_lower for amt_key in ['amt', 'amount', 'value']):
                column_mapping[col] = 'Amount'
            elif any(type_key in col_lower for type_key in ['type', 'transaction type', 'debit/credit']):
                column_mapping[col] = 'Type'
        
        # Rename columns if mapping was found
        if column_mapping:
            df = df.rename(columns=column_mapping)
        
        # Check for required columns
        for col in ['Date', 'Description', 'Amount']:
            if col not in df.columns:
                raise ValueError(f"Required column '{col}' not found in the bank statement.")
        
        # Convert date to datetime format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Add Category column if not exists
        if 'Category' not in df.columns:
            df['Category'] = df['Description'].apply(infer_category)
        
        # Handle rows with NaN dates
        df = df.dropna(subset=['Date'])
        
        return df
    
    except Exception as e:
        print(f"Error loading bank statement: {e}")
        return None

def infer_category(description):
    """
    Automatically categorize a transaction based on its description.
    
    Args:
        description (str): Transaction description
    
    Returns:
        str: Inferred category
    """
    if not isinstance(description, str):
        return "Other"
        
    description = description.lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.lower() in description for keyword in keywords):
            return category
    
    # Default category if no match
    return "Other"

def process_summary(df):
    """
    Process the bank statement dataframe to generate summary statistics.
    
    Args:
        df (pandas.DataFrame): Bank statement dataframe
    
    Returns:
        tuple: (category_sums, income_sum, expense_sum, net)
    """
    # Handle missing Amount values
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
    
    expenses = df[df['Amount'] < 0].copy()
    income = df[df['Amount'] > 0].copy()
    
    # Sum by category
    category_sums = expenses.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)
    
    # Calculate totals
    income_sum = income['Amount'].sum()
    expense_sum = abs(expenses['Amount'].sum())
    net = income_sum - expense_sum
    
    return category_sums, income_sum, expense_sum, net

def breakdown_by_period(df, period='M'):
    """
    Break down expenses by time period and category.
    
    Args:
        df (pandas.DataFrame): Bank statement dataframe
        period (str): Time period - 'M' for monthly, 'W' for weekly, 'D' for daily
    
    Returns:
        pandas.DataFrame: Pivot table with period and category breakdown
    """
    if 'Date' not in df.columns or not pd.api.types.is_datetime64_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
    df['Period'] = df['Date'].dt.to_period(period)
    
    # Create pivot table
    summary = df.pivot_table(
        index='Period',
        columns='Category',
        values='Amount',
        aggfunc='sum',
        fill_value=0
    )
    
    return summary

def export_summary(category_sums, breakdown, out_csv):
    """
    Export summary statistics to a CSV file.
    
    Args:
        category_sums (pandas.Series): Sum of expenses by category
        breakdown (pandas.DataFrame): Expenses broken down by period
        out_csv (str): Output file path
    """
    try:
        with pd.ExcelWriter(out_csv) as writer:
            # Export category summary
            category_sums.to_frame('Amount').to_excel(writer, sheet_name='Category Summary')
            
            # Export time breakdown
            if breakdown is not None:
                breakdown.to_excel(writer, sheet_name='Time Breakdown')
            
        print(f"Summary exported to {out_csv}")
    except Exception as e:
        print(f"Error exporting summary: {e}")

def get_monthly_totals(df):
    """
    Get monthly totals of expenses.
    
    Args:
        df (pandas.DataFrame): Bank statement dataframe
    
    Returns:
        pandas.DataFrame: Monthly totals
    """
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    monthly_totals = df.groupby('Month')['Amount'].sum().reset_index()
    return monthly_totals

def get_top_expenses(df, n=5):
    """
    Get top N highest expenses.
    
    Args:
        df (pandas.DataFrame): Bank statement dataframe
        n (int): Number of top expenses to return
    
    Returns:
        pandas.DataFrame: Top expenses
    """
    expenses = df[df['Amount'] < 0].copy()
    expenses['Amount'] = expenses['Amount'].abs()
    return expenses.nlargest(n, 'Amount')

def calculate_savings_rate(df):
    """
    Calculate savings rate (income - expenses) / income.
    
    Args:
        df (pandas.DataFrame): Bank statement dataframe
    
    Returns:
        float: Savings rate as a percentage
    """
    income = df[df['Amount'] > 0]['Amount'].sum()
    expenses = abs(df[df['Amount'] < 0]['Amount'].sum())
    
    if income > 0:
        savings_rate = (income - expenses) / income * 100
        return round(savings_rate, 2)
    else:
        return 0

def validate_file_extension(filename):
    """
    Check if a file has a valid extension for bank statements.
    
    Args:
        filename (str): Filename to check
    
    Returns:
        bool: True if extension is valid, False otherwise
    """
    valid_extensions = ['.csv', '.xlsx', '.xls']
    _, extension = os.path.splitext(filename.lower())
    return extension in valid_extensions

def get_date_range(df):
    """
    Get the start and end dates from the dataframe.
    
    Args:
        df (pandas.DataFrame): Bank statement dataframe
    
    Returns:
        tuple: (start_date, end_date)
    """
    start_date = df['Date'].min().strftime('%Y-%m-%d')
    end_date = df['Date'].max().strftime('%Y-%m-%d')
    return start_date, end_date