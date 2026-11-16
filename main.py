"""
main.py
Personal Expense Tracker - GUI Version
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from expense import Expense
from expense_manager import ExpenseManager
from budget import Budget

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f4f4f4")

        self.manager = ExpenseManager("data/expenses.json")
        self.budget = Budget("data/budget.json")

        self.create_widgets()
        self.refresh_table()
        self.update_dashboard()

    def create_widgets(self):
        # --- TITLE ---
        title_lbl = tk.Label(self.root, text="Personal Expense Tracker", font=("Arial", 22, "bold"), bg="#f4f4f4")
        title_lbl.pack(pady=10)

        # --- DASHBOARD FRAME ---
        dash_frame = tk.LabelFrame(self.root, text="Dashboard", bg="#f4f4f4", font=("Arial", 10, "bold"))
        dash_frame.pack(fill="x", padx=10, pady=5)

        self.lbl_income = tk.Label(dash_frame, text="Total Income: 0.00", bg="#f4f4f4", font=("Arial", 11))
        self.lbl_income.grid(row=0, column=0, padx=20, pady=10)

        self.lbl_expense = tk.Label(dash_frame, text="Total Expense: 0.00", bg="#f4f4f4", font=("Arial", 11))
        self.lbl_expense.grid(row=0, column=1, padx=20, pady=10)

        self.lbl_balance = tk.Label(dash_frame, text="Balance: 0.00", bg="#f4f4f4", font=("Arial", 11))
        self.lbl_balance.grid(row=0, column=2, padx=20, pady=10)

        self.lbl_month_exp = tk.Label(dash_frame, text="This Month Expense: 0.00", bg="#f4f4f4", font=("Arial", 11))
        self.lbl_month_exp.grid(row=0, column=3, padx=20, pady=10)

        # --- TRANSACTION DETAILS FRAME ---
        input_frame = tk.LabelFrame(self.root, text="Transaction Details", bg="#f4f4f4", font=("Arial", 10, "bold"))
        input_frame.pack(fill="x", padx=10, pady=5)

        # Labels & Entries
        tk.Label(input_frame, text="Name", bg="#f4f4f4").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.ent_name = tk.Entry(input_frame, width=20)
        self.ent_name.grid(row=1, column=0, padx=10, pady=5)

        tk.Label(input_frame, text="Amount ()", bg="#f4f4f4").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.ent_amount = tk.Entry(input_frame, width=15)
        self.ent_amount.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Date (YYYY-MM-DD)", bg="#f4f4f4").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.ent_date = tk.Entry(input_frame, width=15)
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_date.grid(row=1, column=2, padx=10, pady=5)

        tk.Label(input_frame, text="Category", bg="#f4f4f4").grid(row=0, column=3, sticky="w", padx=10, pady=5)
        self.cmb_category = ttk.Combobox(input_frame, values=Expense.CATEGORIES, width=15, state="readonly")
        self.cmb_category.current(0)
        self.cmb_category.grid(row=1, column=3, padx=10, pady=5)

        tk.Label(input_frame, text="Type", bg="#f4f4f4").grid(row=0, column=4, sticky="w", padx=10, pady=5)
        self.cmb_type = ttk.Combobox(input_frame, values=Expense.TYPES, width=12, state="readonly")
        self.cmb_type.current(0)
        self.cmb_type.grid(row=1, column=4, padx=10, pady=5)

        tk.Label(input_frame, text="Payment", bg="#f4f4f4").grid(row=0, column=5, sticky="w", padx=10, pady=5)
        self.cmb_payment = ttk.Combobox(input_frame, values=Expense.PAYMENTS, width=15, state="readonly")
        self.cmb_payment.current(0)
        self.cmb_payment.grid(row=1, column=5, padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(input_frame, bg="#f4f4f4")
        btn_frame.grid(row=2, column=0, columnspan=6, pady=10)

        tk.Button(btn_frame, text="Add", width=12, command=self.add_record).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update Selected", width=15, command=self.update_record).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", width=15, command=self.delete_record).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear Form", width=12, command=self.clear_form).pack(side="left", padx=5)

        # --- SEARCH FRAME ---
        search_frame = tk.Frame(self.root, bg="#f4f4f4")
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Search (ID, name, category, date):", bg="#f4f4f4").pack(side="left", padx=5)
        self.ent_search = tk.Entry(search_frame, width=30)
        self.ent_search.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search_record).pack(side="left", padx=5)
        tk.Button(search_frame, text="Show All", command=self.refresh_table).pack(side="left", padx=5)

        # --- TABLE FRAME ---
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Name", "Amount ()", "Category", "Date", "Type", "Payment Method")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=200)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # --- BUDGET FRAME ---
        budget_frame = tk.LabelFrame(self.root, text="Budget and Analysis", bg="#f4f4f4", font=("Arial", 10, "bold"))
        budget_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(budget_frame, text="Monthly budget ():", bg="#f4f4f4").pack(side="left", padx=5, pady=10)
        self.ent_budget = tk.Entry(budget_frame, width=15)
        self.ent_budget.pack(side="left", padx=5)
        
        tk.Button(budget_frame, text="Set Budget", command=self.set_budget).pack(side="left", padx=5)
        tk.Button(budget_frame, text="Show Analysis", command=self.show_analysis).pack(side="left", padx=5)

        self.lbl_budget_status = tk.Label(budget_frame, text="No monthly budget set.", bg="#f4f4f4", font=("Arial", 10, "italic"))
        self.lbl_budget_status.pack(side="left", padx=20)

    # --- LOGIC METHODS ---

    def update_dashboard(self):
        income, expense, balance, month_exp = self.manager.get_dashboard_stats()
        self.lbl_income.config(text=f"Total Income: {income:.2f}")
        self.lbl_expense.config(text=f"Total Expense: {expense:.2f}")
        self.lbl_balance.config(text=f"Balance: {balance:.2f}")
        self.lbl_month_exp.config(text=f"This Month Expense: {month_exp:.2f}")
        
        # Budget limit check
        if self.budget.monthly_budget > 0:
            if month_exp > self.budget.monthly_budget:
                self.lbl_budget_status.config(text=f" Exceeded by {month_exp - self.budget.monthly_budget:.2f}!", fg="red")
            else:
                self.lbl_budget_status.config(text=f"Remaining: {self.budget.monthly_budget - month_exp:.2f}", fg="green")
        else:
            self.lbl_budget_status.config(text="No monthly budget set.", fg="black")

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        records = data if data is not None else self.manager.get_all()
        
        for e in records:
            self.tree.insert("", "end", values=(e.expense_id, e.name, f"{e.amount:.2f}", e.category, e.date, e.t_type, e.payment))

    def clear_form(self):
        self.ent_name.delete(0, "end")
        self.ent_amount.delete(0, "end")
        self.ent_date.delete(0, "end")
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.cmb_category.current(0)
        self.cmb_type.current(0)
        self.cmb_payment.current(0)

    def add_record(self):
        name = self.ent_name.get().strip()
        amount = self.ent_amount.get().strip()
        date = self.ent_date.get().strip()
        cat = self.cmb_category.get()
        t_type = self.cmb_type.get()
        payment = self.cmb_payment.get()

        # Auto-generate ID based on count
        new_id = str(max([int(i) for i in self.manager.used_ids if i.isdigit()] + [0]) + 1)

        try:
            self.manager.add_expense(new_id, name, amount, cat, date, t_type, payment)
            self.refresh_table()
            self.update_dashboard()
            self.clear_form()
            messagebox.showinfo("Success", "Transaction added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item['values']
        
        self.clear_form()
        self.ent_name.insert(0, values[1])
        self.ent_amount.insert(0, values[2])
        self.cmb_category.set(values[3])
        self.ent_date.delete(0, "end")
        self.ent_date.insert(0, values[4])
        self.cmb_type.set(values[5])
        self.cmb_payment.set(values[6])

    def update_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to update.")
            return
        
        expense_id = self.tree.item(selected[0])['values'][0]
        
        try:
            self.manager.update_expense(
                str(expense_id), 
                self.ent_name.get().strip(), 
                self.ent_amount.get().strip(), 
                self.cmb_category.get(), 
                self.ent_date.get().strip(), 
                self.cmb_type.get(), 
                self.cmb_payment.get()
            )
            self.refresh_table()
            self.update_dashboard()
            self.clear_form()
            messagebox.showinfo("Success", "Record updated!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return
            
        expense_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            self.manager.delete_expense(str(expense_id))
            self.refresh_table()
            self.update_dashboard()
            self.clear_form()

    def search_record(self):
        query = self.ent_search.get().strip()
        if not query:
            self.refresh_table()
            return
        
        results = self.manager.search(query)
        self.refresh_table(results)

    def set_budget(self):
        try:
            amount = float(self.ent_budget.get().strip())
            self.budget.set_budget(amount)
            self.update_dashboard()
            messagebox.showinfo("Success", "Budget updated!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def show_analysis(self):
        summary = self.manager.get_analysis()
        
        analysis_text = f"Total Transactions: {summary['count']}\n\n"
        analysis_text += f"Total Income: {summary['total_income']:.2f}\n"
        analysis_text += f"Total Expense: {summary['total_expense']:.2f}\n"
        analysis_text += f"Average Expense: {summary['average_expense']:.2f}\n"
        analysis_text += f"Highest Single Expense: {summary['highest_expense']:.2f}\n\n"
        
        analysis_text += "--- Category-wise Expenses ---\n"
        for cat, total in summary['category_totals'].items():
            analysis_text += f"{cat}: {total:.2f}\n"
            
        messagebox.showinfo("NumPy Analysis Report", analysis_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()