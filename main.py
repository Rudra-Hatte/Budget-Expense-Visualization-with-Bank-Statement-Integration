import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys

def load_bank_statement(csv_file):
    try:
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        sys.exit(1)

def process_expenses(df):
    # Assumes columns like: Date, Description, Amount, Category
    # You may need to adjust these column names to match your CSV.
    if 'Category' not in df.columns or 'Amount' not in df.columns:
        print("CSV must contain 'Category' and 'Amount' columns.")
        sys.exit(1)
    expenses = df[df['Amount'] < 0]  # Negative amounts as expenses
    category_sums = expenses.groupby('Category')['Amount'].sum().abs()
    return category_sums

def visualize_expenses(category_sums):
    plt.figure(figsize=(8, 8))
    category_sums.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Expense Distribution by Category')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Budget & Expense Visualization with Bank Statement Integration")
    parser.add_argument('csv_file', type=str, help='Path to the bank statement CSV file')
    args = parser.parse_args()

    df = load_bank_statement(args.csv_file)
    category_sums = process_expenses(df)
    print("Expense summary by category:")
    print(category_sums)
    visualize_expenses(category_sums)

if __name__ == '__main__':
    main()