import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
import os
import numpy as np

# Optionally import for interactive features
try:
    import seaborn as sns
except ImportError:
    sns = None

CATEGORY_KEYWORDS = {
    "Groceries": ["market", "grocery", "supermarket", "store"],
    "Dining": ["restaurant", "cafe", "coffee", "dining", "food"],
    "Transport": ["uber", "lyft", "metro", "bus", "train", "taxi", "fuel", "petrol"],
    "Entertainment": ["cinema", "movie", "netflix", "spotify", "music", "game"],
    "Utilities": ["electric", "water", "gas", "internet", "utility", "phone"],
    "Shopping": ["amazon", "mall", "shopping", "store", "clothes"],
    "Income": ["salary", "deposit", "refund", "credit", "interest"],
    # Add more as needed
}

def infer_category(description):
    desc = str(description).lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in desc for kw in keywords):
            return cat
    return "Other"

def load_bank_statement(csv_file):
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        sys.exit(1)
    try:
        df = pd.read_csv(csv_file)
        if 'Category' not in df.columns:
            print("No 'Category' column, inferring categories...")
            df['Category'] = df['Description'].apply(infer_category)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        sys.exit(1)

def process_summary(df):
    expenses = df[df['Amount'] < 0].copy()
    income = df[df['Amount'] > 0].copy()
    category_sums = expenses.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)
    income_sum = income['Amount'].sum()
    expense_sum = expenses['Amount'].sum()
    net = income_sum + expense_sum
    return category_sums, income_sum, -expense_sum, net

def breakdown_by_period(df, period='M'):
    df['Period'] = df['Date'].dt.to_period(period)
    summary = df.groupby(['Period', 'Category'])['Amount'].sum().unstack(fill_value=0)
    return summary

def visualize_all(category_sums, income_sum, expense_sum, net, breakdown, output=None):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Pie chart
    category_sums.plot(kind='pie', autopct='%1.1f%%', ax=axes[0,0], legend=False)
    axes[0,0].set_title('Expense Distribution by Category')
    axes[0,0].set_ylabel('')
    
    # Income vs Expense
    axes[0,1].bar(['Income', 'Expense', 'Net'], [income_sum, expense_sum, net], color=['green','red','blue'])
    axes[0,1].set_title('Income vs Expense')
    axes[0,1].set_ylabel('Amount')

    # Trend over time
    if breakdown is not None:
        breakdown.plot(ax=axes[1,0], kind='bar', stacked=True)
        axes[1,0].set_title('Expenses by Category per Period')
        axes[1,0].set_ylabel('Amount')
        axes[1,0].legend(loc='best')
    else:
        axes[1,0].axis('off')

    # Hide fourth subplot or use for future
    axes[1,1].axis('off')

    plt.tight_layout()
    if output:
        plt.savefig(output)
        print(f"Visualization saved to {output}")
    else:
        plt.show()

def export_summary(category_sums, breakdown, out_csv):
    category_sums.to_csv(out_csv.replace('.csv','_category_summary.csv'))
    if breakdown is not None:
        breakdown.to_csv(out_csv.replace('.csv','_breakdown.csv'))
    print(f"Summaries exported to CSV.")

def main():
    parser = argparse.ArgumentParser(description="Advanced Budget & Expense Visualization Tool")
    parser.add_argument('csv_file', type=str, help='Path to the bank statement CSV file')
    parser.add_argument('--breakdown', type=str, choices=['M','W','D'], default='M', help='Breakdown period: M=monthly, W=weekly, D=daily')
    parser.add_argument('--export', type=str, help='Export summary to specified CSV file')
    parser.add_argument('--output', type=str, help='Save visualization to file instead of showing')
    args = parser.parse_args()

    df = load_bank_statement(args.csv_file)
    category_sums, income_sum, expense_sum, net = process_summary(df)
    print("Expense summary by category:")
    print(category_sums)
    print("\nTotal income: {:.2f}\nTotal expenses: {:.2f}\nNet: {:.2f}".format(income_sum, expense_sum, net))

    breakdown = breakdown_by_period(df, args.breakdown)
    print("\nBreakdown by period:\n", breakdown)

    if args.export:
        export_summary(category_sums, breakdown, args.export)
    
    visualize_all(category_sums, income_sum, expense_sum, net, breakdown, args.output)

if __name__ == '__main__':
    main()