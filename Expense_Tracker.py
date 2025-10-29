import json
import os
import random
from datetime import datetime

expenses = []
file_name = "expenses_data.json"
budget_file = "budget.json"

def set_budget():
    """Allow user to set their own budget limit."""
    print("\nLet's set your monthly budget limit!")
    while True:
        try:
            value = input("Enter your budget limit in Rs (press Enter for default Rs.5000): ")
            if not value.strip():
                print("Default budget Rs.5000 selected.")
                return 5000.0
            value = float(value)
            if value <= 0:
                print("Please enter a positive amount.")
                continue
            print(f"Budget limit to set Rs.{value}")
            return value
        except ValueError:
            print("Invalid input! Please enter a number.")

def load_budget():
    if os.path.exists(budget_file):
        try:
            with open(budget_file, "r") as f:
                data = json.load(f)
                print(f"Loaded your saved budget limit: Rs.{date['budget']}")
                return data["budget"]
        except Exception:
            pass
    budget = set_budget()
    with open(budget_file, "w") as f:
        json.dump({"budget": budget}, f)
    return budget

budget_limit = load_budget()


try:
    with open(file_name, "r") as file:
        expenses = json.load(file)
        print(f"Loaded {len(expenses)} previouus expenses successfully!")
except FileNotFoundError:
    expenses = []
    print("No previous data found. Starting fresh!")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def save_data():
    try:
        with open(file_name, "w") as file:
            json.dump(expenses, file, indent=4)
        print("Data saved successfully!")
    except Exception as e:
        print("Error saving data:", e)

def random_quote():
    quotes = [
        "Save money, live better!"
        "A rupee saved is a rupee earned.",
        "Track it today, thank yourself tomorrow!",
        "Spend smart, not hard!"
    ]

    print(random.choice(quotes))

def check_budget():
    total = sum(exp["amount"] for exp in expenses)
    if total > budget_limit:
        print(f"Warning: You exceeded your monthly budget of Rs.{budget_limit}!")
    else:
        print(f"Current total Rs.{total} is within your budget (limit: Rs.{budget_limit})")

def auto_category(name):
    name = name.lower()
    if any(word in name for word in ["pizza", "burger", "snack", "food", "restaurant"]):
        return "Food"
    elif any(word in name for word in ["bus", "taxi", "uber", "train", "fuel"]):
        return "Travel"
    elif any(word in name for word in ["shirt", "jeans", "shoe", "cloth", "shopping"]):
        return "Shopping"
    elif any(word in name for word in ["bills", "electricity", "uber", "wifi", "mobile"]):
        return "Bills"
    else:
        return "Other"

def add_expense():
    try:
        name = input("Enter expense name: ")
        amount = float(input("Enter amount: "))
        auto_cat = auto_category(name)
        print(f"Auto detected category: {auto_cat}")
        category = input(f"Enter category (default {auto_cat}): ").capitalize() or auto_cat
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expenses.append({"name": name, "amount": amount, "category": category, "date": date})
        print(f"Added {name} - Rs.{amount} ({category}) on {date}")
        check_budget()
        save_data()
    except ValueError:
        print("Invalid amount! Please enter a number.")

def view_all_expenses():
    """View all expenses."""
    if not expenses:
        print("No expenses yet.")
        return
    print("\nAll Expenses:")
    for i, exp in enumerate(expenses, start=1):
        print(f"{i} {exp['name']} - Rs.{exp['amount']} ({exp['amount']}) {exp['date']}")
    random_quote()

def search_by_category():
    """Search and show expenses by category with total & average."""
    if not expenses:
        print("No data to available.")
        return
    cat = input("Enter category to search: ").capitalize()
    found = [exp for exp in expenses if exp["category"] == cat]
    if not found:
        print(f"No expenses found in '{cat}' category.")
    else:
        print(f"\nExpenses in '{cat}' category:")
        for i, exp in enumerate(found, start=1):
            print(f"{i}. {exp['name']} - Rs.{exp['amount']}")
        total = sum(exp["amount"] for exp in found)
        avg = total / len(found)
        print(f"Total = Rs.{total} | Average per item = Rs.{avg:.2f}")

def category_summary():
    """Show total expense per category."""
    if not expenses:
        print("No expense yet.")
        return
    print("\nCategory Summary:")
    summary = {}
    for exp in expenses:
        cat = exp["category"]
        summary[cat] = summary.get(cat, 0) + exp["amount"]
    for cat, amt in summary.items():
        print(f"{cat}: Rs.{amt}")
    random_quote()

def monthly_summary():
    """Show total, average, highest, lowest, expense for a month."""
    if not expenses:
        print("No data available.")
        return
    month = input("Enter month (YYYY-MM): ")
    monthly = [exp for exp in expenses if exp["date"].startswith(month)]
    if not monthly:
        print("No expenses for this month.")
        return
    total = sum(exp["amount"] for exp in monthly)
    avg = total / len(monthly)
    highest = max(monthly, key=lambda x: x["amount"])
    lowest = min(monthly, key=lambda x: x["amount"])
    print(f"\n Summary for {month}")
    print(f"Highest = {highest['name']} (Rs.{highest['name']})")
    print(f"Lowest = {lowest['name']} (Rs.{lowest['name']})")
    random_quote()

def export_report():
    """Export all data to text report."""
    if not expenses:
        print("No data to export.")
        return
    with open("export_report.txt", "w") as file:
        for exp in expenses:
            file.write(f"{exp['date']} | {exp['name']} | Rs.{exp['amount']} | {exp['category']}\n")
    print("Report exported as successfully as 'export_report.txt'!")

def delete_expense():
    """Delete an expense by its name."""
    if not expenses:
        print("No expenses to delete.")
        return
    name = input("Enter expense name to delete: ")
    for exp in expenses:
        if exp['name'].lower() == name.lower():
            expenses.remove(exp)
            print(f"Expense '{name}' deleted successfully!")
            save_data()
            break
    else:
        print("Expense not found!")

def main_menu():
    while True:
        print("\n" + "=" * 40)
        print("WELCOME TO ADVANCED EXPENSE TRACKER")
        print("=" * 40)
        print("1. Add Expense")
        print("2. View All Expense")
        print("3. Search by Category")
        print("4. Category Summary")
        print("5. Monthly Summary")
        print("6. Export Report")
        print("7. Delete Expense")
        print("8. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all_expenses()
        elif choice == "3":
            search_by_category()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            monthly_summary()
        elif choice == "6":
            export_report()
        elif choice == "7":
            delete_expense()
        elif choice == "8":
            save_data()
            print("Exiting.... Thanks for using Expense Tracker!")
            break
        else:
            print("Invalid choice! Please enter in between 1 and 8.")

if __name__ == "__main__":
    main_menu()
    



