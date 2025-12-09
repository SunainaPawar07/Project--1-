NAME-Sunaina Pawar 
ENROLLMENT NO-1057EC231038
PROJECT TITLE-EXPENSE TRACKER

import csv
from datetime import datetime
import os

# --- Configuration ---
EXPENSE_FILE = 'expenses.csv'
FIELDNAMES = ['date', 'category', 'amount', 'description']

# --- File Operations ---

def initialize_file():
    """Checks if the expense file exists and creates it with headers if not."""
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def load_expenses():
    """Loads all expenses from the CSV file into a list of dictionaries."""
    expenses = []
    try:
        with open(EXPENSE_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert amount from string (in file) to float (in memory)
                try:
                    row['amount'] = float(row['amount'])
                    expenses.append(row)
                except ValueError:
                    print(f"Skipping malformed entry: {row}")
    except FileNotFoundError:
        pass # initialize_file will handle creating it later
    return expenses

def save_expense(expense):
    """Appends a single new expense to the CSV file."""
    with open(EXPENSE_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(expense)

# --- Core Logic ---

def add_expense():
    """Prompts the user for expense details and saves it."""
    print("\n--- Add New Expense ---")
    
    # Date Input
    date_str = input("Enter date (YYYY-MM-DD, leave blank for today): ").strip()
    if not date_str:
        expense_date = datetime.now().strftime('%Y-%m-%d')
    else:
        try:
            # Validate format
            datetime.strptime(date_str, '%Y-%m-%d')
            expense_date = date_str
        except ValueError:
            print("❌ Invalid date format. Using today's date.")
            expense_date = datetime.now().strftime('%Y-%m-%d')

    # Category Input
    category = input("Enter category (e.g., Food, Transport, Rent): ").strip()
    if not category:
        category = "Other"

    # Amount Input
    while True:
        try:
            amount = float(input("Enter amount spent: "))
            if amount <= 0:
                print("Amount must be positive.")
                continue
            break
        except ValueError:
            print("❌ Invalid input. Please enter a number for the amount.")
            
    # Description Input
    description = input("Enter a brief description: ").strip()

    new_expense = {
        'date': expense_date,
        'category': category.title(), # Title case for clean display
        'amount': amount,
        'description': description
    }
    
    save_expense(new_expense)
    print("✅ Expense recorded successfully!")

def view_summary(expenses):
    """Calculates and prints the total and category-wise spending."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    total_spent = sum(item['amount'] for item in expenses)
    category_summary = {}

    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        category_summary[category] = category_summary.get(category, 0) + amount

    print("\n--- Expense Summary ---")
    print(f"Total Spent: **Rs{total_spent:,.2f}**")
    print("\nSummary by Category:")
    
    # Sort categories by amount spent (highest first)
    sorted_summary = sorted(category_summary.items(), key=lambda item: item[1], reverse=True)
    
    for category, amount in sorted_summary:
        percentage = (amount / total_spent) * 100
        print(f"- {category}: **Rs{amount:,.2f}** ({percentage:.1f}%)")

def view_details(expenses):
    """Prints a detailed list of all recorded expenses."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- Detailed Expense List ---")
    print(f"{'Date':<10} | {'Category':<15} | {'Amount':>10} | Description")
    print("-" * 50)
    for exp in expenses:
        print(f"{exp['date']:<10} | {exp['category']:<15} | {exp['amount']:>10,.2f} | {exp['description']}")



def main():
    """Main function to run the expense tracker."""
    initialize_file()
    
    while True:
        print("\n--- Expense Tracker Menu ---")
        print("1. Add New Expense")
        print("2. View Summary")
        print("3. View Detailed List")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        expenses = load_expenses() # Reload expenses on each loop to include new additions

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_summary(expenses)
        elif choice == '3':
            view_details(expenses)
        elif choice == '4':
            print(" Thank you for using the Expense Tracker. Goodbye!")
            break
        else:
            print(" Invalid choice. Please select a number from 1 to 4.")

if __name__ == "__main__":
    main()