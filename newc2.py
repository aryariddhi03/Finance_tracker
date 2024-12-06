import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json

# Initialize variables
income = 0.0
expenses = []
savings = 0.0
budgets = {category: 0.0 for category in ["Food", "Transport", "Utilities", "Entertainment", "Other"]}

# Load transactions data from file
def load_data():
    global income, expenses, savings
    try:
        with open('transactions.json', 'r') as file:
            data = json.load(file)
            income = data.get('income', 0.0)
            expenses = data.get('expenses', [])
            savings = data.get('savings', 0.0)
    except (FileNotFoundError, json.JSONDecodeError):
        reset_data()

# Save transactions data to file
def save_data():
    global income, expenses, savings
    savings = income - sum(expense['amount'] for expense in expenses)  # Update savings before saving
    data = {
        'income': income,
        'expenses': expenses,
        'savings': savings
    }
    with open('transactions.json', 'w') as file:
        json.dump(data, file)

# Load budgets data
def load_budgets():
    global budgets
    try:
        with open('budgets.json', 'r') as file:
            budgets = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        save_budgets()

# Save budgets data
def save_budgets():
    global budgets
    with open('budgets.json', 'w') as file:
        json.dump(budgets, file)

def set_budget():
    global budgets
    try:
        category = budget_category_var.get()
        if category == "Select category":
            messagebox.showerror("Error", "Please select a valid category.")
            return
        amount = float(budget_amount_entry.get())
        budgets[category] = amount
        save_budgets()
        messagebox.showinfo("Success", f"Budget for {category} set to {amount}!")
        budget_amount_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Invalid budget amount. Please enter a valid number.")

# Reset data to default values
def reset_data():
    global income, expenses, savings
    income, expenses, savings = 0.0, [], 0.0
    save_data()
    update_summary()

# Clear placeholder on click
def clear_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="black")

# Add income
def add_income():
    global income
    try:
        amount = float(income_entry.get())
        income += amount
        save_data()  # Save updated data
        messagebox.showinfo("Success", f"Income of {amount} added successfully!")
        income_entry.delete(0, tk.END)
        update_summary()
    except ValueError:
        messagebox.showerror("Error", "Invalid income amount. Please enter a valid number.")

# Add expense
def add_expense():
    global expenses
    description = Expense_entry.get()
    try:
        amount = float(amount_entry.get()) 
        category = Expense_category_var.get()
        if category == "Select category":
            messagebox.showerror("Error", "Please select a valid category.")
            return
        expense = {"description": description, "amount": amount, "category": category}
        expenses.append(expense)
        save_data()  # Save updated data

        # Check if expense exceeds the budget
        category_total = sum(e['amount'] for e in expenses if e['category'] == category)
        if category_total > budgets.get(category, 0.0):
            messagebox.showwarning(
                "Budget Alert",
                f"Expenses for {category} have exceeded the budget of {budgets[category]:.2f}!"
            )

        messagebox.showinfo("Success", "Expense added successfully!")
        Expense_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END) 
        update_summary()
    except ValueError:
        messagebox.showerror("Error", "Invalid expense amount. Please enter a valid number.")

# Calculate savings
def calculate_savings():
    global income, expenses, savings
    savings = income - sum(expense['amount'] for expense in expenses)
    save_data()  # Save updated data
    messagebox.showinfo("Savings", f"Your total savings are: {savings}")
    update_summary()

def generate_expense_chart():
    """
    Generates a pie chart of expenses by category using Matplotlib.
    If there are no expenses, it notifies the user.
    """
    import matplotlib.pyplot as plt

    try:
        # Check if expenses list is empty
        if not expenses:
            messagebox.showinfo("Info", "No expenses found. Please add transactions first.")
            return

        # Organize expenses by category
        categories = set(expense.get('category', 'Uncategorized') for expense in expenses)
        category_expenses = {category: 0.0 for category in categories}

        for expense in expenses:
            amount = expense.get('amount', 0.0)
            category = expense.get('category', 'Uncategorized')

            # Validate that the amount is numeric
            if not isinstance(amount, (int, float)):
                raise ValueError(f"Invalid amount in expense: {expense}")

            category_expenses[category] += amount

        # Validate that there is data to plot
        if all(value == 0 for value in category_expenses.values()):
            messagebox.showinfo("Info", "No expenses found to plot.")
            return

        # Prepare data for the pie chart
        labels = list(category_expenses.keys())
        values = list(category_expenses.values())

        # Create the pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c7b3e5'],
            startangle=140,
        )
        plt.title('Expenses by Category', fontsize=14)
        plt.axis('equal')  # Ensure the pie chart is a circle
        plt.show()

    except ValueError as e:
        messagebox.showerror("Error", f"Data validation error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Delete all transactions
def delete_all_transactions():
    reset_data()
    messagebox.showinfo("Success", "All transactions deleted successfully!")

# Update summary
def update_summary():
    income_label.config(text=f"Income: {income}")
    expenses_label.config(text=f"Expenses: {sum(expense['amount'] for expense in expenses)}")
    savings_label.config(text=f"Savings: {savings}")

# GUI Setup
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("1000x700")
root.config(bg="#eaeaea")

# Background image for entire window
background_image_path = r"C:\Users\riddh\OneDrive\Desktop\New\finance.jpg"
background_image = Image.open(background_image_path)
background_image = background_image.resize((1000, 700), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)



# Main frame for content
main_frame = tk.Frame(root, bg="#ffffff", bd=5)
main_frame.place(relx=0.04, rely=0.04, relwidth=0.8, relheight=0.8)

# Background image for main frame
frame_bg_image_path = r"C:\Users\riddh\OneDrive\Desktop\New\finance2.jpg"
frame_bg_image = Image.open(frame_bg_image_path)
frame_bg_image = frame_bg_image.resize((800, 560), Image.Resampling.LANCZOS)
frame_bg_photo = ImageTk.PhotoImage(frame_bg_image)
frame_bg_label = tk.Label(main_frame, image=frame_bg_photo)
frame_bg_label.place(relwidth=1, relheight=1)

# Budget Section
budget_label_title = tk.Label(main_frame, text="Budget:", font=("Arial", 14, "bold"), bg="#ffffff")
budget_label_title.place(x=50, y=70)

budget_category_var = tk.StringVar(value="Category")
budget_category_menu = ttk.Combobox(main_frame, textvariable=budget_category_var, state="readonly", font=("Arial", 12))
budget_category_menu['values'] = ["Food", "Transport", "Utilities", "Entertainment", "Other"]
budget_category_menu.place(x=200, y=105)

budget_amount_entry = tk.Entry(main_frame, fg="gray", font=("Arial", 14), width=20)
budget_amount_entry.insert(0, "Enter Budget")
budget_amount_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, budget_amount_entry, "Enter budget"))
budget_amount_entry.place(x=200, y=70)

set_budget_button = tk.Button(main_frame, text="Set Budget", command=set_budget, font=("Arial", 12), bg="#6c5ce7", fg="white")
set_budget_button.place(x=500, y=105)

# Income Section
income_label_title = tk.Label(main_frame, text="Add Income:", font=("Arial", 14, "bold"), bg="#ffffff")
income_label_title.place(x=50, y=30)

income_entry = tk.Entry(main_frame, fg="gray", font=("Arial", 14), width=20)
income_entry.insert(0, "Enter Income")
income_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, income_entry, "Enter income"))
income_entry.place(x=200, y=30)

add_income_button = tk.Button(main_frame, text="Add Income", command=add_income, font=("Arial", 12), bg="#6c5ce7", fg="white")
add_income_button.place(x=500, y=30)

# Expenses Section
Expense_label_title = tk.Label(main_frame, text="Add Expense:", font=("Arial", 14, "bold"), bg="#ffffff")
Expense_label_title.place(x=50, y=290)

Expense_entry = tk.Entry(main_frame, fg="gray", font=("Arial", 14), width=20)
Expense_entry.insert(0, "Enter Description")
Expense_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, Expense_entry, "Enter Description"))
Expense_entry.place(x=200, y=290)

amount_entry = tk.Entry(main_frame, fg="gray", font=("Arial", 14), width=20)
amount_entry.insert(0, "Enter Amount")
amount_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, amount_entry, "Enter Amount"))
amount_entry.place(x=200, y=330)

Expense_category_var = tk.StringVar(value="Select category")
Expense_category_menu = ttk.Combobox(main_frame, textvariable=Expense_category_var, state="readonly", font=("Arial", 12))
Expense_category_menu['values'] = ["Food", "Transport", "Utilities", "Entertainment", "Other"]
Expense_category_menu.place(x=200, y=370)

add_expense_button = tk.Button(main_frame, text="Add Expense", command=add_expense, font=("Arial", 12), bg="#6c5ce7", fg="white")
add_expense_button.place(x=500, y=370)

# Summary Section
income_label = tk.Label(main_frame, text=f"Income: {income}", font=("Arial", 12), bg="#ffffff")
income_label.place(x=50, y=450)

expenses_label = tk.Label(main_frame, text=f"Expenses: {sum(expense['amount'] for expense in expenses)}", font=("Arial", 12), bg="#ffffff")
expenses_label.place(x=50, y=480)

savings_label = tk.Label(main_frame, text=f"Savings: {savings}", font=("Arial", 12), bg="#ffffff")
savings_label.place(x=50, y=510)

# Buttons for chart generation, savings calculation, and delete all
calculate_savings_button = tk.Button(main_frame, text="Calculate Savings", command=calculate_savings, font=("Arial", 12), bg="#ff6347", fg="white")
calculate_savings_button.place(x=500, y=450)

generate_chart_button = tk.Button(main_frame, text="Generate Chart", command=generate_expense_chart, font=("Arial", 12), bg="#ff6347", fg="white")
generate_chart_button.place(x=500, y=490)

delete_all_button = tk.Button(main_frame, text="Delete All", command=delete_all_transactions, font=("Arial", 12), bg="#ff6347", fg="white")
delete_all_button.place(x=500, y=530)

# Load data
load_data()
load_budgets()
update_summary()

# Run the app
root.mainloop()
