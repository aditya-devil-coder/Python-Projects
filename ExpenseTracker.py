import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import csv
from matplotlib.ticker import FuncFormatter

class ExpenseTracker:
    def __init__(self, data_file="expenses.csv", budget_file="budgets.json"):
        self.data_file = data_file
        self.budget_file = budget_file
        self.categories = ["Food", "Transportation", "Housing", "Entertainment", "Utilities", 
                          "Healthcare", "Education", "Shopping", "Travel", "Other"]
        
        # Load or create expense data
        if os.path.exists(data_file):
            self.expenses = pd.read_csv(data_file)
            # Convert date strings to datetime objects
            self.expenses['Date'] = pd.to_datetime(self.expenses['Date'])
        else:
            self.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
            self.expenses['Date'] = pd.to_datetime(self.expenses['Date'])
        
        # Load or create budget data
        if os.path.exists(budget_file):
            with open(budget_file, 'r') as f:
                self.budgets = json.load(f)
        else:
            self.budgets = {category: 0 for category in self.categories}
            self._save_budgets()
    
    def _save_expenses(self):
        """Save expenses to CSV file"""
        self.expenses.to_csv(self.data_file, index=False)
    
    def _save_budgets(self):
        """Save budgets to JSON file"""
        with open(self.budget_file, 'w') as f:
            json.dump(self.budgets, f)
    
    def add_expense(self, date, category, amount, description):
        """Add a new expense entry"""
        if category not in self.categories:
            print(f"Error: Category must be one of {self.categories}")
            return False
        
        try:
            # Convert string date to datetime if needed
            if isinstance(date, str):
                date = pd.to_datetime(date)
                
            # Create new expense entry
            new_expense = pd.DataFrame({
                'Date': [date],
                'Category': [category],
                'Amount': [float(amount)],
                'Description': [description]
            })
            
            # Append to existing expenses
            self.expenses = pd.concat([self.expenses, new_expense], ignore_index=True)
            self._save_expenses()
            
            # Check for budget overage and alert if needed
            self._check_budget_alert(category)
            return True
            
        except Exception as e:
            print(f"Error adding expense: {e}")
            return False
    
    def set_budget(self, category, amount):
        """Set budget for a specific category"""
        if category not in self.categories:
            print(f"Error: Category must be one of {self.categories}")
            return False
        
        try:
            self.budgets[category] = float(amount)
            self._save_budgets()
            return True
        except Exception as e:
            print(f"Error setting budget: {e}")
            return False
    
    def _check_budget_alert(self, category):
        """Check if the category has exceeded its budget and alert if so"""
        # Get current month's expenses for this category
        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        month_expenses = self.expenses[
            (self.expenses['Date'] >= month_start) & 
            (self.expenses['Category'] == category)
        ]
        
        total_spent = month_expenses['Amount'].sum()
        budget = self.budgets[category]
        
        if budget > 0 and total_spent > budget:
            print(f"⚠️ ALERT: You've exceeded your {category} budget!")
            print(f"Budget: ${budget:.2f}, Spent: ${total_spent:.2f}, Overage: ${total_spent - budget:.2f}")
            return True
        return False
    
    def get_summary(self, period='monthly'):
        """Generate expense summary for the specified period"""
        if self.expenses.empty:
            return "No expenses recorded yet."
        
        now = datetime.now()
        
        if period == 'weekly':
            # Get last 7 days
            start_date = now - timedelta(days=7)
            period_name = f"Weekly ({start_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')})"
        elif period == 'monthly':
            # Get current month
            start_date = datetime(now.year, now.month, 1)
            period_name = f"Monthly ({now.strftime('%B %Y')})"
        else:
            print("Invalid period. Use 'weekly' or 'monthly'.")
            return None
        
        # Filter expenses for the period
        period_expenses = self.expenses[self.expenses['Date'] >= start_date]
        
        if period_expenses.empty:
            return f"No expenses recorded for this {period} period."
        
        # Calculate total and category-wise spending
        total_spent = period_expenses['Amount'].sum()
        category_summary = period_expenses.groupby('Category')['Amount'].sum()
        
        # Format summary as string
        summary = f"===== {period_name} Expense Summary =====\n"
        summary += f"Total Spent: ${total_spent:.2f}\n\n"
        summary += "Spending by Category:\n"
        
        for category in self.categories:
            if category in category_summary:
                amount = category_summary[category]
                percentage = (amount / total_spent) * 100
                summary += f"{category}: ${amount:.2f} ({percentage:.1f}%)\n"
                
                # Add budget comparison if budget exists
                if self.budgets[category] > 0:
                    budget = self.budgets[category]
                    remaining = budget - amount
                    status = "Under budget" if remaining >= 0 else f"OVER BUDGET by ${abs(remaining):.2f}"
                    summary += f"  Budget: ${budget:.2f}, {status}\n"
        
        return summary
    
    def visualize_expenses(self, period='monthly'):
        """Create visualization of expenses"""
        if self.expenses.empty:
            print("No expenses to visualize.")
            return
        
        now = datetime.now()
        
        if period == 'weekly':
            start_date = now - timedelta(days=7)
            title = f"Weekly Expenses ({start_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')})"
        elif period == 'monthly':
            start_date = datetime(now.year, now.month, 1)
            title = f"Monthly Expenses ({now.strftime('%B %Y')})"
        else:
            print("Invalid period. Use 'weekly' or 'monthly'.")
            return
        
        # Filter expenses for the period
        period_expenses = self.expenses[self.expenses['Date'] >= start_date]
        
        if period_expenses.empty:
            print(f"No expenses recorded for this {period} period.")
            return
        
        # Setup the figure with multiple subplots
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle(title, fontsize=16)
        
        # 1. Pie chart of expenses by category
        ax1 = fig.add_subplot(2, 2, 1)
        category_totals = period_expenses.groupby('Category')['Amount'].sum()
        
        # Only include categories with expenses
        categories_with_expenses = category_totals[category_totals > 0]
        
        if not categories_with_expenses.empty:
            ax1.pie(categories_with_expenses, labels=categories_with_expenses.index, 
                   autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            ax1.set_title('Expenses by Category')
        else:
            ax1.text(0.5, 0.5, "No category data to display", 
                    horizontalalignment='center', verticalalignment='center')
        
        # 2. Bar chart comparing to budget
        ax2 = fig.add_subplot(2, 2, 2)
        categories = []
        spent_amounts = []
        budget_amounts = []
        
        for category in self.categories:
            if category in category_totals and self.budgets[category] > 0:
                categories.append(category)
                spent_amounts.append(category_totals[category])
                budget_amounts.append(self.budgets[category])
        
        if categories:
            x = np.arange(len(categories))
            width = 0.35
            
            ax2.bar(x - width/2, spent_amounts, width, label='Spent')
            ax2.bar(x + width/2, budget_amounts, width, label='Budget')
            
            ax2.set_title('Spent vs Budget by Category')
            ax2.set_xticks(x)
            ax2.set_xticklabels(categories, rotation=45, ha='right')
            ax2.legend()
            
            # Format y-axis as currency
            def currency_formatter(x, pos):
                return f'${x:.0f}'
            
            ax2.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
        else:
            ax2.text(0.5, 0.5, "No budget data to compare", 
                    horizontalalignment='center', verticalalignment='center')
        
        # 3. Daily spending trend
        ax3 = fig.add_subplot(2, 1, 2)
        daily_expenses = period_expenses.groupby(pd.Grouper(key='Date', freq='D'))['Amount'].sum()
        
        # Fill in missing days with zeros
        date_range = pd.date_range(start=start_date, end=now)
        daily_expenses = daily_expenses.reindex(date_range, fill_value=0)
        
        ax3.plot(daily_expenses.index, daily_expenses.values, marker='o')
        ax3.set_title('Daily Spending Trend')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Amount ($)')
        ax3.grid(True, linestyle='--', alpha=0.7)
        
        # Format x-axis dates
        fig.autofmt_xdate()
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()
        
    def export_to_csv(self, filename='expense_export.csv'):
        """Export expenses to a CSV file"""
        if self.expenses.empty:
            print("No expenses to export.")
            return False
        
        try:
            # Create a copy of the DataFrame to avoid modifying the original
            export_df = self.expenses.copy()
            
            # Ensure date is in string format for CSV
            export_df['Date'] = export_df['Date'].dt.strftime('%Y-%m-%d')
            
            export_df.to_csv(filename, index=False)
            print(f"Expenses successfully exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting expenses: {e}")
            return False
            
    def list_expenses(self, n=10):
        """List the most recent n expenses"""
        if self.expenses.empty:
            print("No expenses recorded yet.")
            return
            
        recent_expenses = self.expenses.sort_values('Date', ascending=False).head(n)
        
        print(f"\n===== Most Recent {len(recent_expenses)} Expenses =====")
        for i, (_, expense) in enumerate(recent_expenses.iterrows(), 1):
            print(f"{i}. Date: {expense['Date'].strftime('%Y-%m-%d')}, "
                  f"Category: {expense['Category']}, "
                  f"Amount: ${expense['Amount']:.2f}, "
                  f"Description: {expense['Description']}")


# Example usage function to demonstrate the application
def run_example():
    # Initialize the expense tracker
    tracker = ExpenseTracker()
    
    print("\n===== EXPENSE TRACKER WITH DATA ANALYSIS =====")
    
    # Set some example budgets
    tracker.set_budget("Food", 300)
    tracker.set_budget("Transportation", 150)
    tracker.set_budget("Entertainment", 100)
    
    # Add some example expenses
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=6)
    
    # Add expenses if the tracker doesn't have any
    if tracker.expenses.empty:
        tracker.add_expense(today, "Food", 25.50, "Grocery shopping")
        tracker.add_expense(today, "Entertainment", 15.00, "Movie ticket")
        tracker.add_expense(yesterday, "Transportation", 30.00, "Gas")
        tracker.add_expense(yesterday, "Food", 45.75, "Dinner with friends")
        tracker.add_expense(yesterday - timedelta(days=1), "Utilities", 120.00, "Electricity bill")
        tracker.add_expense(last_week, "Shopping", 85.20, "New shoes")
        tracker.add_expense(last_week, "Food", 12.30, "Lunch")
        tracker.add_expense(last_week + timedelta(days=1), "Healthcare", 50.00, "Prescription")
    
    # Show main menu
    while True:
        print("\n===== MAIN MENU =====")
        print("1. Add Expense")
        print("2. Set Budget")
        print("3. List Recent Expenses")
        print("4. View Monthly Summary")
        print("5. View Weekly Summary")
        print("6. Visualize Monthly Expenses")
        print("7. Visualize Weekly Expenses")
        print("8. Export Expenses to CSV")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-8): ")
        
        if choice == '1':
            date_str = input("Enter date (YYYY-MM-DD) or press enter for today: ")
            date = datetime.now() if date_str == "" else datetime.strptime(date_str, "%Y-%m-%d")
            
            print("\nCategories:")
            for i, category in enumerate(tracker.categories, 1):
                print(f"{i}. {category}")
            
            cat_choice = int(input("\nSelect category number: "))
            category = tracker.categories[cat_choice - 1] if 1 <= cat_choice <= len(tracker.categories) else "Other"
            
            amount = float(input("Enter amount: $"))
            description = input("Enter description: ")
            
            if tracker.add_expense(date, category, amount, description):
                print("Expense added successfully!")
        
        elif choice == '2':
            print("\nCategories:")
            for i, category in enumerate(tracker.categories, 1):
                print(f"{i}. {category}")
            
            cat_choice = int(input("\nSelect category number to set budget: "))
            if 1 <= cat_choice <= len(tracker.categories):
                category = tracker.categories[cat_choice - 1]
                amount = float(input(f"Enter monthly budget for {category}: $"))
                
                if tracker.set_budget(category, amount):
                    print(f"Budget for {category} set to ${amount:.2f}")
            else:
                print("Invalid category selection!")
        
        elif choice == '3':
            n = int(input("How many recent expenses to show? "))
            tracker.list_expenses(n)
        
        elif choice == '4':
            summary = tracker.get_summary('monthly')
            print(f"\n{summary}")
        
        elif choice == '5':
            summary = tracker.get_summary('weekly')
            print(f"\n{summary}")
        
        elif choice == '6':
            tracker.visualize_expenses('monthly')
        
        elif choice == '7':
            tracker.visualize_expenses('weekly')
        
        elif choice == '8':
            filename = input("Enter export filename (default: expense_export.csv): ")
            if not filename:
                filename = "expense_export.csv"
            if tracker.export_to_csv(filename):
                print(f"Data exported to {filename} successfully!")
        
        elif choice == '0':
            print("Thank you for using the Expense Tracker!")
            break
        
        else:
            print("Invalid choice! Please enter a number between 0 and 8.")


# Run the example if the script is executed directly
if __name__ == "__main__":
    run_example()