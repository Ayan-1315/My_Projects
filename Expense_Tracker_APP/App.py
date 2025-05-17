import os
from Expense import Expense
import pandas as pd
from datetime import datetime

# Path to store the CSV file
expense_file_path = 'Expenses.csv'
budget_file_path = 'Budget.csv'  # File to track monthly budget

# Budget for each month
MONTHLY_BUDGET = 5000

def main():
    print("💸 Running expense tracker!")
    
    # Check if the month has changed and reset the budget if needed
    reset_monthly_budget_if_needed()
    
    # Get user input for expense
    expense = user_expense()

    # Update expense to a CSV file
    update_expense(expense)
    
    # Read file and summarize expenses
    summarize_expense(expense_file_path)


def user_expense():
    print("\n💸 Getting user expense!")
    expense_name = input("\nEnter the name of the Expense: ")
    expense_amount = input("\nEnter the amount of the Expense: ")
    print(f"\nYou spent on {expense_name} of ₹{expense_amount}")
    
    expense_categories = [
        "Travel",
        "Food",
        "Fun",
        "Home",
        "Work"
    ]
    
    while True:
        print("Select a category -->")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i+1}. {category_name}")
        
        value_range = f"[1 to {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
        
        if selected_index in range(len(expense_categories)):
            expense_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=expense_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid Category. Please choose correctly -->")
        

def update_expense(expense):
    print(f"\n💸 Saving user expense: {expense} to {expense_file_path}")
    
    # Create a DataFrame from the expense object and append it to the CSV
    expense_data = {
        'Name': [expense.name],
        'Category': [expense.category],
        'Amount': [f"₹ {expense.amount}"],
        'Date': [datetime.now().strftime("%Y-%m-%d")],  # Store the date of expense
        'Month': [datetime.now().strftime("%B-%Y")]     # Store the month of expense
    }
    
    df = pd.DataFrame(expense_data)
    
    # Append to CSV if it exists, else create a new one
    df.to_csv(expense_file_path, mode='a', header=not os.path.exists(expense_file_path), index=False)
    

def summarize_expense(expense_file_path):
    print("\n💸 Summarizing the expenses!\n")
    
    try:
        df = pd.read_csv(expense_file_path, error_bad_lines=False)  
        print(df)
        print("\nCategory and Amount columns:\n")
        
        # Removing the currency symbol to convert the 'Amount' column into numeric
        df['Amount'] = df['Amount'].replace({'₹': '', ',': ''}, regex=True).astype(float)

        # Calculate total spent per category
        total_spent_per_category(df)
        
        # Filter expenses for the current month
        current_month = datetime.now().strftime("%B-%Y")
        current_month_expenses = df[df['Month'] == current_month]
        
        # Calculate the total amount spent for the current month
        total_amount = current_month_expenses['Amount'].sum()
        print(f"\nTotal Amount Spent This Month ({current_month}): ₹ {total_amount}\n")
        
        # Load the monthly budget from the file or use the default
        budget_amount = get_monthly_budget()
        
        if total_amount < budget_amount:
            print(green(f"Your budget left: ₹ {budget_amount - total_amount}"))
        else:
            print(red(f"Your budget is overspent by ₹ {total_amount - budget_amount}"))
        
    except FileNotFoundError:
        print("No expenses found yet.")
    except pd.errors.ParserError as e:
        print(f"Error reading CSV file: {e}")


def total_spent_per_category(df):
    print("\n💸 Total Spend Per Category:\n")
    
    # Group the data by 'Category' and calculate the sum of 'Amount'
    category_totals = df.groupby('Category')['Amount'].sum()
    
    # Print the results
    for category, total in category_totals.items():
        print(f"{category}: ₹ {total}")
    return category_totals


def reset_monthly_budget_if_needed():
    current_month = datetime.now().strftime("%B-%Y")
    
    if os.path.exists(budget_file_path):
        df_budget = pd.read_csv(budget_file_path)
        last_tracked_month = df_budget['Month'].iloc[-1]  # Get the last tracked month

        # If the month has changed, reset the budget
        if last_tracked_month != current_month:
            print(f"\n💸 New month detected: {current_month}. Resetting the budget.")
            update_monthly_budget(current_month)
    else:
        # If the budget file doesn't exist, create it for the current month
        update_monthly_budget(current_month)


def update_monthly_budget(current_month):
    print(f"\n💸 Setting a budget of ₹ {MONTHLY_BUDGET} for {current_month}")
    
    budget_data = {
        'Month': [current_month],
        'Budget': [MONTHLY_BUDGET]
    }
    
    df_budget = pd.DataFrame(budget_data)
    
    # Append to CSV if it exists, else create a new one
    df_budget.to_csv(budget_file_path, mode='a', header=not os.path.exists(budget_file_path), index=False)


def get_monthly_budget():
    current_month = datetime.now().strftime("%B-%Y")
    
    if os.path.exists(budget_file_path):
        df_budget = pd.read_csv(budget_file_path)
        current_month_budget = df_budget[df_budget['Month'] == current_month]['Budget'].values
        
        if current_month_budget:
            return current_month_budget[0]
    
    # Return default budget if no entry exists for the current month
    return MONTHLY_BUDGET


def green(text):
    return f"\033[92m{text}\033[0m"


def red(text):
    return f"\033[31m{text}\033[0m"


if __name__ == "__main__":
    main()
